from .UserSessionTypes import UserSessionTypes
from .SessionAbstract import SessionAbstract
import signal, time
import logging
from .FileMonitor import FileMonitor
from . import BGConfig
import queue
from .fileconverters import getFileConverter
from .corpusreaders import getCurrentReader
from .classifiers import ClassifierClusterWithScoring
import os
from .autotaggers import getActiveTagger, NLTKPlainTextTagger, XmlAutoTagger
from .tools.ClassifierMixin import SentenceSelections
from .tools.SMCorpusDocumentReader import SMCorpusDocumentReader
import pandas as pd
from .data.api import DBSession
from .data import models as models
from core.corpusgens import getCorpusGenerator

logger = logging.getLogger(__name__)

class BackgroundSession(SessionAbstract):
    """A background session which continues to run until a 
    terminate signal is received. """
    
    __slots__ = [
        '_bExit',
        '_fileMonitor',
        '_fileQueue',
        ]

    def __init__(self):
        SessionAbstract.__init__(self, UserSessionTypes.Background)
        self._bExit = False
        signal.signal(signal.SIGINT, self.__exitOnSignal)
        signal.signal(signal.SIGTERM, self.__exitOnSignal)
        self.__initialize()
        return

    def __exitOnSignal(self, signum, frame):
        self._bExit = True
        return

    def __initialize(self):
        logger.info("Initializing....")
        logger.info("Current directory: " + os.getcwd())

        BGConfig.CreateFolders()

        self._fileQueue = queue.Queue()
        self._fileMonitor = FileMonitor(BGConfig.ConvertLocation, self._fileQueue)
        logger.info("Training corpus....")
        tags = DBSession.Create().getTags() # all tag definitions
        corpusreader = getCurrentReader(BGConfig.CorpusLocation, tags)
        for sel in SentenceSelections:
            if sel == SentenceSelections.UseDocument:
                self._buildSaveDocumentClassifier(corpusreader, tags)
            elif sel == SentenceSelections.UseSentence:
                self._buildSaveSentClassifier(corpusreader, tags)
            elif sel == SentenceSelections.UsePhrase:
                self._buildSavePhraseClassifier(corpusreader, tags)
            else:
                continue
        logger.info("Training corpus completed. Processing any documents in dropped folder.")
        self._processAvailableDroppedFiles()

    def _buildSaveDocumentClassifier(self, reader, tagset):
        if BGConfig.RebuildTrainingset or not ClassifierClusterWithScoring.IsPickled(SentenceSelections.UseDocument):
            clfcluster = ClassifierClusterWithScoring(SentenceSelections.UseDocument, tagset)
            data = reader.Documents()
            data = list(map(list, zip(*data)))
            tags  = pd.Series(data=data[0])
            features = pd.Series(data=data[1])
            clfcluster.Fit(SentenceSelections.UseDocument, features, tags)
            # pickle classifer
            ClassifierClusterWithScoring.Pickle(clfcluster)

    def _buildSaveSentClassifier(self, reader, tagset):
        if BGConfig.RebuildTrainingset or not ClassifierClusterWithScoring.IsPickled(SentenceSelections.UsePhrase):
            clfcluster = ClassifierClusterWithScoring(SentenceSelections.UseSentence, tagset)
            data = reader.Sents()
            data = list(map(list, zip(*data)))
            tags  = pd.Series(data=data[0])
            features = pd.Series(data=data[1])
            clfcluster.Fit(SentenceSelections.UseSentence, features, tags)
            # pickle classifer
            ClassifierClusterWithScoring.Pickle(clfcluster)

    def _buildSavePhraseClassifier(self, reader, tagset):
        if BGConfig.RebuildTrainingset or not ClassifierClusterWithScoring.IsPickled(SentenceSelections.UsePhrase):
            clfcluster = ClassifierClusterWithScoring(SentenceSelections.UsePhrase, tagset)
            data = reader.Phrases()
            data = list(map(list, zip(*data)))
            tags  = pd.Series(data=data[0])
            features = pd.Series(data=data[1])
            clfcluster.Fit(SentenceSelections.UsePhrase, features, tags)
            # pickle classifer
            ClassifierClusterWithScoring.Pickle(clfcluster)

    def _processAvailableDroppedFiles(self):
        """ Populate any files in drop folder."""
        #TODO: Try a new thread for this.
        for a, b, c in os.walk(BGConfig.ConvertLocation, topdown=False):
            if a == BGConfig.DropLocation:
                logger.warn("Didn't find any subdirectories for suppliers in " + BGConfig.ConvertLocation)
                break
            for fd in c:
                self.__OnNewFileCreated(os.path.join(a, fd))

    def __OnNewFileCreated(self, filePath):
        logger.info(filePath)
        try:
            _, ext = os.path.splitext(filePath)
            if ext == ".xml":
                self.__AutoTagNewFile(filePath, "xml")
            else:
                with getFileConverter(filePath) as pages:
                    # file converters always returns a list of tuples of pagenumber and text content
                    self.__AutoTagNewFile(filePath, pages)
            self.__MoveToStorageFolder(filePath)
        except Exception as e:
            logger.error(e)
            strError = str(e)
            if "PDF document is encrypted" in strError:
                self.__MoveToFailedFolder(filePath)
                return
            # try again
            #if isinstance(e, PermissionError):
            #    self._processAvailableDroppedFiles()

    def _getSupplId(self, filePath):
        return filePath.split(os.path.sep)[-2]

    def __MoveToFailedFolder(self, filePath):
        newPath = os.path.join(BGConfig.FailedLocation, self._getSupplId(filePath), os.path.basename(filePath))
        dir = os.path.split(newPath)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(newPath):
            os.rename(filePath, newPath)
        else:
            os.remove(filePath)
        return

    def __MoveToStorageFolder(self, filePath):
        newPath = os.path.join(BGConfig.StoreLocation, self._getSupplId(filePath), os.path.basename(filePath))
        dir = os.path.split(newPath)[0]
        if not os.path.exists(dir):
            os.makedirs(dir)
        if not os.path.exists(newPath):
            os.rename(filePath, newPath)
        else:
            os.remove(filePath)
        return


    def __AutoTagNewFile(self, uploadedFilePath, content):
        classifiers = {
            SentenceSelections.UseDocument: (ClassifierClusterWithScoring.Unpickle(SentenceSelections.UseDocument), None),
            SentenceSelections.UseSentence: (ClassifierClusterWithScoring.Unpickle(SentenceSelections.UseSentence), None),
            SentenceSelections.UsePhrase: (ClassifierClusterWithScoring.Unpickle(SentenceSelections.UsePhrase), None),
        }
        try:
            if content == "xml":
                autoTagger = XmlAutoTagger(classifiers)
                autoTagger.TagContent(uploadedFilePath)
                supplId = autoTagger.getSupplierId()
                fileName = autoTagger.getFileName()
            else:
                autoTagger = getActiveTagger(classifiers)
                if isinstance(autoTagger, NLTKPlainTextTagger):
                    autoTagger.TagContent(str(uploadedFilePath))
                else:
                    autoTagger.TagContent(str(content))
                # extract supplierId from uploadedFilePath (note in drop folder, files are stored inside a folder for each supplier)
                supplId = self._getSupplId(uploadedFilePath)
                fileName = os.path.basename(uploadedFilePath)
        except Exception as e:
            logger.error(e)
            raise e
        # persist tag meta in the database
        '''
        1. Save Domain
        2. Save Sentences
        3. Save phrases
        4. Save tagged file in drop location (using tags generated from 2 and 3, tag the document)
        '''
        try:
            db = DBSession.Create()
            # begin a transaction
            domain = autoTagger.getDomain()
            # TOP one is most common
            domain = domain[0]
            # save domain and document info
            doc = self._persistDocumentInfo(db.getSession(), int(supplId), domain, fileName)
        
            taggedSents = autoTagger.getSents()
            if taggedSents:
                self._persistMetaData('Sentence', db.getSession(), doc, taggedSents)
            taggedPhrases = autoTagger.getPhrases()
            if taggedPhrases:
                self._persistMetaData('Phrase', db.getSession(), doc, taggedPhrases)
            
            db.Commit()
        except Exception as e:
            logger.error(e)
            raise e

        try:
            corpusGen = getCorpusGenerator(autoTagger, content)
            if not os.path.exists(os.path.join(BGConfig.ReviewLocation, supplId)):
                os.makedirs(os.path.join(BGConfig.ReviewLocation, supplId))

            writefilepath = os.path.join(BGConfig.ReviewLocation, int(supplId), os.path.basename(uploadedFilePath))
            corpusGen.write(writefilepath)
        except Exception as e:
            logger.error(e)
            raise e

    def _persistMetaData(self, tagClassName, dbsession, doc, data):
        ''' DocMetaData:
            Id = Column(BigInteger, primary_key=True)
            DocId = Column(BigInteger, ForeignKey("Documents.DocId"))
            TagId = Column(BigInteger, ForeignKey("Tags.TagId"))
            TagClassId = Column(BigInteger, ForeignKey("TagClasses.ClassId"))
            Score = Column(Float, nullable=True)
            TagData = Column(String, nullable=False)
            PageNo = Column(Integer, nullable=True)
            Offset = Column(Integer, nullable=True)
        '''


        def getTag(tag):
            return dbsession.query(models.Tag).filter(models.Tag.Name==tag).first()

        def getTagClass(classname):
            return dbsession.query(models.TagClass).filter(models.TagClass.Name==classname).first()

        metaInfoList = [models.DocMetaData( tag=getTag(tagname), tagClass=getTagClass(tagClassName), Score=score, TagData=sent, PageNo=pno, Offset=0)\
          for pno, tagname, score, sent in data ]
        
        doc.TagMetaData.extend(metaInfoList)


    def _persistDocumentInfo(self, dbsession, supplierId, docDomain, docPath):
        ''' Document:
            DocId = Column(BigInteger, primary_key=True)
            SupplId = Column(BigInteger, ForeignKey('Suppliers.SupplId'))
            Domain = Column(String)
            FilePath = Column(String)
        '''
        # first check if the document already exists
        docs = dbsession.query(models.Document).\
            filter(models.Document.SupplId==supplierId, models.Document.FilePath.ilike('%' + docPath))
        for doc in docs:
            dbsession.query(models.DocMetaData).filter(models.DocMetaData.Doc == doc) \
                .delete(synchronize_session=False)
            dbsession.delete(doc)

        doc = models.Document(SupplId=supplierId, Domain=docDomain, FilePath=docPath)
        dbsession.add(doc)
        return doc

    def run(self):
        while True:
            if not self._fileQueue.empty():
                fileinfo = self._fileQueue.get_nowait()
                self.__OnNewFileCreated(fileinfo)
            else:
                time.sleep(1)
            if self._bExit:
                logger.warning("Exiting background process main thread.")
                break
        return

    def closeSession(self):
        return


