from .tools.ClassifierMixin import SentenceSelections, ClassifierMixin
import nltk as nk
from . import BGConfig
from nltk.corpus.reader.plaintext import PlaintextCorpusReader
import os, io
import logging
import xml.etree.cElementTree as et;


logger = logging.getLogger(__name__)


class AutoTaggerBase(object):
    __slots__ = [
        '_classifiers'
        ]
    def __init__(self, classifiers):
        self._classifiers = classifiers
        return

    def TagContent(self, contents): # contents is a list of tuples as pagenum and page content.
        raise NotImplementedError()

    def getDomain(self):
        return "getdomain"

    def getPhrases(self):
        return []

    def getSents(self):
        pass # yield ret

    def _getTrigrams(self, sent):
        trigram_measures = nk.collocations.TrigramAssocMeasures()
        trigrammer = nk.TrigramCollocationFinder.from_words(ClassifierMixin.wordTokenize(sent))
        scored = trigrammer.score_ngrams(trigram_measures.raw_freq)
        for trigram, score in scored:
            posTagged = nk.pos_tag(list(trigram))
            word, pos = posTagged[0]
            if pos[0] in ['V', 'N', 'J']:
                yield ' '.join(map(str, trigram))

class DefaultTagger(AutoTaggerBase):
    __slots__ = [
        '_contents'
        ]

    def __init__(self, classifiers):
        AutoTaggerBase.__init__(self, classifiers)
        return

    def TagContent(self, contents): # simply return true since plan to yield
        self._contents = contents
        # clean up content
        if isinstance(self._contents, list):
            for idx in range(len(self._contents)):
                self._contents[idx] = (self._contents[idx][0], self._fixContent(self._contents[idx][1])) # each one is tuple (pagenum, pagecontent)
        elif isinstance(self._contents, str):
            self._contents = self._fixContent(self._contents)
        else:
            self._contents = str(self._contents)
        return True

    def _fixContent(self, content):
        if not content:
            return content
        content = content.replace('\n', ' ')
        return content

    def getDomain(self):
        # build a single unit of content from all pages
        strOut = ''
        if isinstance(self._contents, list):
            import io
            joinedContent = io.StringIO(self._contents[0][1])
            if len(self._contents) > 1:
                for idx in range(1, len(self._contents)):
                    joinedContent.write(' ')
                    joinedContent.write(self._contents[idx][1])
            strOut = joinedContent.getvalue()
        else:
            strOut = self._contents
        classifier, acheck = self._classifiers.get(SentenceSelections.UseDocument)
        if not classifier:
            return 'NON'
        domain = classifier.Predict(strOut, bestTag=True)
        return domain

    def getPhrases(self):
        return self._getPredictions(SentenceSelections.UsePhrase)

    def getSents(self):
        # if content is a list, then it is tuples of pageno and page text
        # We will split page text to sentences also
        # returns tuple(pageno, tag, score, sent)
        return self._getPredictions(SentenceSelections.UseSentence)

    def _getPredictions(self, sel):
        classifier, acheck = self._classifiers.get(sel)
        if  not classifier:
            return list()
        clfResults = []
        if isinstance(self._contents, list):
            for pno, ptext in self._contents:
                sents = ptext.split('.')
                for idx in range(len(sents)):
                    sent = sents[idx].strip()
                    if not sent:
                        continue
                    if sel == SentenceSelections.UsePhrase:
                        for trigram in self._getTrigrams(sent):
                            tag, score = classifier.Predict(trigram, bestTag=True)
                            if tag in BGConfig.Phrase_Tags:
                                clfResults.append((pno, tag, round(score, 4), trigram))
                    else:
                        tag, score = classifier.Predict(sent, bestTag=True)
                        clfResults.append((pno, tag, round(score, 4), sent))
        elif (self._contents, str):
            sents = self._contents.split('.')
            for idx in range(len(sents)):
                sent = sents[idx].strip()
                if not sent:
                    continue
                if sel == SentenceSelections.UsePhrase:
                    for trigram in self._getTrigrams(sent):
                        tag, score = classifier.Predict(trigram, bestTag=True)
                        if tag in BGConfig.Phrase_Tags:
                            clfResults.append((0, tag, round(score, 4), trigram))
                else:
                    tag, score = classifier.Predict(sent, bestTag=True)
                    clfResults.append((0, tag, round(score, 4), sent))
        return clfResults

class NLTKPlainTextTagger(AutoTaggerBase):
    __slots__ = [
        '_classifiers',
        '_ptext_reader'
        ]
    def __init__(self, classifiers):
        self._classifiers = classifiers
        return

    def TagContent(self, filePath): # file path.
        # break filepath into root and basename
        root, fileid = (os.path.dirname(filePath), os.path.basename(filePath))
        try:
            self._ptext_reader = PlaintextCorpusReader(root, fileid, encoding="latin1")
            self._ptext_reader.raw()
        except Exception as e:
            logger.warn(e)
            self._ptext_reader = PlaintextCorpusReader(root, fileid, encoding="iso-8859-15")
        return 

    def getDomain(self):
        # build a single unit of content from all pages
        strOut = self._ptext_reader.raw()
        classifier, acheck = self._classifiers.get(SentenceSelections.UseDocument)
        if not classifier:
            return 'NON'
        domain = classifier.Predict(strOut, bestTag=True)
        return domain

    def getPhrases(self):
        return self._getPredictions(SentenceSelections.UsePhrase)

    def getSents(self):
        # if content is a list, then it is tuples of pageno and page text
        # We will split page text to sentences also
        # returns tuple(pageno, tag, score, sent)
        return self._getPredictions(SentenceSelections.UseSentence)

    def _getPredictions(self, sel):
        classifier, acheck = self._classifiers.get(sel)
        if  not classifier:
            return list()
        clfResults = []

        for sent in self._ptext_reader.sents():
            if not sent:
                continue
            sent = ' '.join(sent)
            if sel == SentenceSelections.UsePhrase:
                for trigram in self._getTrigrams(sent):
                    tag, score = classifier.Predict(trigram, bestTag=True)
                    if tag in BGConfig.Phrase_Tags:
                        clfResults.append((0, tag, round(score, 4), trigram))
            else:
                tag, score = classifier.Predict(sent, bestTag=True)
                clfResults.append((0, tag, round(score, 4), sent))
        return clfResults

class XmlAutoTagger(AutoTaggerBase):

    __slots__ = [
        '_root',
        '_phraseCheckList'
        ]

    def __init__(self, classifiers):
        AutoTaggerBase.__init__(self, classifiers)
        self._root = None
        self._phraseCheckList = ['@', '.'] # email or web domain
        return
 
    def TagContent(self, filePath): # contents is a list of tuples as pagenum and page content.
        '''
        filename : conversioninfo/fileinfo/name
        supplid = conversioninfo/fileinfo/supplierid
        page with num = conversioninfo/page[@num]
        .... blocks and lines ....
        converted by = conversioninfo/convertedby
        '''
        tree = et.parse(filePath)
        self._root = tree.getroot()
        return

    def getFileName(self):
        return self._root.find("fileinfo/name").text.strip()

    def getSupplierId(self):
        return self._root.find("fileinfo/supplierid").text.strip()

    def getGeneratedFrom(self):
        # Is the xml generated from direct text extraction or OCR extraction 
        return self._root.find("convertedby").text.strip()

    def getDomain(self):
        # Combine all texts from all pages and clean up and classify
        ostrContent = io.StringIO()
        pages = self._root.findall("page")
        sorted(pages, key = lambda e : int(e.attrib.get("num")))
        if self.getGeneratedFrom() == "ocr":
            for i, p in enumerate(pages):
                ostrContent.write(p.text.strip())
                ostrContent.write("\n")
        else:
            # go through page and blocks and then lines
            pass
        classifier, acheck = self._classifiers.get(SentenceSelections.UseDocument)
        if not classifier:
            return 'NON'
        domain = classifier.Predict(ostrContent.getvalue(), bestTag=True)
        return domain

    def getPhrases(self):
        pass #yield return
    
    def _sortPage(self, a):
        return int(a.attrib.get("num"))

    def _sortBlock(self, a):
        return int(a.attrib.get("num"))

    def _sortLine(self, a):
        i = int(a.attrib.get("order"))
        return i

    def getSents(self):
        classifier, acheck = self._classifiers.get(SentenceSelections.UseSentence)
        clfResults = []
        pages = self._root.findall("page")
        pages = sorted(pages, key = self._sortPage)
        if self.getGeneratedFrom() == "ocr":
            for i, p in enumerate(pages):
                txt = p.text
                ostr = io.StringIO()
                for c in iter(txt):
                    if c == '.':
                        strval = ostr.getvalue().strip()
                        if self._doBasicValidation(strval)[0]:
                            logger.info(strval)
                            clfResults.extend(
                                 [(i, tag, round(score, 4), strval) for tag, score in classifier.Predict(strval).items()]
                                )
                        ostr = io.StringIO()
                    else:
                        ostr.write(c)
                strval = ostr.getvalue().strip()
                if self._doBasicValidation(strval)[0]:
                    logger.info(strval)
                    clfResults.extend(
                            [(0, tag, round(score, 4), strval) for tag, score in classifier.Predict(strval).items()]
                        )

        else:
            # go through page and blocks and then lines
            for i, p in enumerate(pages):
                blocks = p.findall("block")
                blocks = sorted(blocks, key=self._sortBlock)
                for b in blocks:
                    lines = b.findall("line")
                    lines = sorted(lines, key=self._sortLine)
                    ostr = io.StringIO()
                    for l in lines:
                        for c in l.findall("content"):
                            ostr.write(c.text.strip())
                            ostr.write(" ")
                        strval = ostr.getvalue()
                    if strval:
                        #logger.info(strval)
                        for sent in strval.split('.'):
                            sent = sent.strip()
                            if self._doBasicValidation(sent)[0]:
                                d = classifier.Predict(sent)
                                for tag, score in d.items():
                                    if score > 0.3:
                                        clfResults.append((i, tag, score, sent))

        return clfResults

    def _doBasicValidation(self, phrase):
        # TODO: Keep expanding this.
        # 1. if the phrase is a single word or if the word not contains @ or . then ignore
        if not phrase:
            return (False, phrase)
        if ' ' not in phrase and any(c in phrase for c in self._phraseCheckList):
            return (True, phrase)
        if '.' in phrase:
            return (True, phrase)
        if ' ' not in phrase:
            return (False, phrase)
        return (True, phrase)


def getActiveTagger(classifier):
    return DefaultTagger(classifier)
    #return NLTKPlainTextTagger(classifier)