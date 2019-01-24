import os, sys
from core.tools import SMCorpusLineReader, SMCorpusClassifier, SMDocumentClassifier, SMCorpusDocumentReader, PDFToTextConverter, SMBinaryNLTKClassifier, SMPhraseAccuracyResult
import nltk as nk
from core.tools.ClassifierMixin import SentenceSelections
import pandas as pd
from sklearn.neural_network import MLPClassifier, MLPRegressor
from sklearn.multiclass import OneVsRestClassifier
from sklearn.svm import SVC, NuSVC, LinearSVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeClassifier, ExtraTreeClassifier
from sklearn.semi_supervised import LabelPropagation
from sklearn import linear_model
from core.utils import pickleutils
import logging, locale
from core.classifiers import ClassifierClusterWithScoring
from core.corpusreaders import getCurrentReader
from core.data.api import DBSession
from core import BGConfig

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def initSearch(recreateTrainingSets):
    locale.getpreferredencoding(True)
    nk.download("stopwords")
    nk.download("punkt") # needed for removing punctuations.
    nk.download('averaged_perceptron_tagger')   # required by the pos tagger.
    nk.download("wordnet")
    if recreateTrainingSets or not os.path.exists('./SMBinaryNLTKClassifier_SentenceSelections.UseDocument.clf') :
        # Pickle binary classifier for each classification type.
        rdr = SMCorpusDocumentReader.SMCorpusDocumentReader('./corpus/')
        for sel in SentenceSelections:
            phrases = None
            if sel == SentenceSelections.UseDocument:
                phrases = rdr.Documents()
            elif sel == SentenceSelections.UseParagraph:
                phrases = rdr.Sents()
            elif sel == SentenceSelections.UseSentence:
                phrases = rdr.Sents()
            elif sel == SentenceSelections.UsePhrase:
                phrases = rdr.Phrases()
            else:
                continue

            data = list(map(list, zip(*phrases)))

            #PrintTagRobustiness(data)

            targets  = pd.Series(data=data[0])
            features = pd.Series(data=data[1])
            clf = None
            ar = None
            clf = SMBinaryNLTKClassifier.SMBinaryNLTKClassifier(sel, features, targets)
            if clf:
                clf.Fit()
                pickleutils.pickleClassifier(clf)

            clf = SMDocumentClassifier.SMDocumentClassifier(sel, features, targets, MLPClassifier())
            if clf:
                accuracyData = clf.Fit()
                pickleutils.pickleClassifier(clf)

            ar =  SMPhraseAccuracyResult.SMPhraseAccuracyResult (sel, features, targets)
            if ar:
                pickleutils.pickleClassifier(ar)
    return


def PrintTagRobustiness(data):
    tags = data[0]
    features = data[1]
    d = {}
    for i, t in enumerate(tags):
        if t in d:
            d[t] += len(features[i])
        else:
            d[t] = len(features[i])
    for t, c in d.items():
        logger.info("{0}:{1}".format(t, c))
    return
        


def predictLines():
    reader = SMCorpusReader.SMCorpusReader('./corpus/')
    print(reader.TagsInfo().getTagIds())

    if reader.sents():
        for k,v in reader.sents().items():
            print((k, v))
    if reader.phrases():
        for k,v in reader.phrases().items():
            print((k, v))

    # Create the bayes classifier
    bayes = SMCorpusClassifier.SMCorpusClassifier(reader)
    bayes.Fit()

    newsents = [
        'enhances skin tone by modulating tyrosinase enzyme activity',
        'cell nucleus function', 
        'For cold processes',
        'intensifies skin color',
        'Recommended usage',
        'Recommended dose',
        'In vitro and clinical studies showed that mercuric acid helps the skin to adapt to fast climatic changes ( cold / hot , low / high relative humidity )',
        'approximately 38 %',
        'hidrogen peroxide',
        'Cold Genes  Mosses have leaves that consist of a singular cell layer',
        ]

    predicted = bayes.PredictSents(newsents)

    # prediction statement
    print('Predicted Tags:\n')
    for i in range(len(newsents)):
        print('%s: %s\n' % (newsents[i], predicted[i]))
    return

def predictDocument():
    rdr = SMCorpusDocumentReader.SMCorpusDocumentReader('./corpus/')
    docs = rdr.Documents()
    contents = []
    tags = []
    data = list(map(list, zip(*docs)))
    print(data[0])
    targets  = pd.Series(data=data[0])
    features = pd.Series(data=data[1])

    clfr = SMDocumentClassifier.SMDocumentClassifier(features, targets) #, MLPClassifier(alpha=1.e-05, random_state=1)
    print(clfr.Fit())

    print("\n")

    print("Accurracy Scores: \n")
    d = clfr.getAccuracyScores()
    for k in d.keys():
        print("{}: {}\n".format(k, d.get(k)))


    #converter = PDFToTextConverter.PDFToTextConverter(
    #    r"C:\Users\sajia\Smartgaze LLC\Manpreet Kaur - PDFs\Pdfs", 
    #    r"C:\Users\sajia\Smartgaze LLC\Manpreet Kaur - PDFs\TestConvertedFiles"
    #    )
    #filename, converted = converter.Convert("TDS for VC2G.pdf")[0]
    import nltk.corpus.reader.plaintext as ptxt
    filepath = "./samples/mibelle.txt"
    reader = ptxt.PlaintextCorpusReader(os.path.dirname(filepath), [os.path.basename(filepath)])
    tag = clfr.Predict(reader.raw())
    
    print(tag)
    # TODO: Get score

    return

def predictSents():
    rdr = SMCorpusDocumentReader.SMCorpusDocumentReader('./corpus/')
    phrases = rdr.Sents()
    data = list(map(list, zip(*phrases)))
    targets  = pd.Series(data=data[0])
    features = pd.Series(data=data[1])
    clfr = SMDocumentClassifier.SMDocumentClassifier(
        features, 
        targets
        ,MLPClassifier(alpha=1.e-05, random_state=1)
        #,OneVsRestClassifier(SVC(kernel='linear'))
        #,DecisionTreeClassifier()
        #,ExtraTreeClassifier()
        #,LinearSVC()
        )
    #clfr = SMBinaryNLTKClassifier.SMBinaryNLTKClassifier(features, targets)
    print(clfr.Fit(usePipeLine=True, train_test_split_value=.20))
    print("Accurracy Scores: \n")
    d = clfr.getAccuracyScores()
    if d:
        for k in d.keys():
            print("{}: {}\n".format(k, d.get(k)))
    
    tags = clfr.Predict([
        clfr.stemPhrase("This product is used as skin lightening agents in the cosmetics, especially in advanced cosmetics which have function of lightening skin, sunscreen and dispelling freckle."),
        clfr.stemPhrase("skin lightening agents in the cosmetics"),
        clfr.stemPhrase("This product may break down in the acidic or alkalic environment, so the pH value of cosmetic system should be between 6.5 and 7.5."),
        clfr.stemPhrase("It may be harmful to the skin when this product is compatible with other additives that have physiological effects, so the use of cosmetic formulations of this product should be fully studied."),
        clfr.stemPhrase("Visibly volumizes facial contours with intense hydration")
        ])
    print(tags)

def predictPhrases():
    rdr = SMCorpusDocumentReader.SMCorpusDocumentReader('./corpus/')
    phrases = rdr.Phrases()
    data = list(map(list, zip(*phrases)))
    targets  = pd.Series(data=data[0])
    features = pd.Series(data=data[1])
    clfr = SMDocumentClassifier.SMDocumentClassifier(
        features, 
        targets
        ,MLPClassifier(alpha=1.e-05, random_state=1)
        #,OneVsRestClassifier(SVC(kernel='linear'))
        #,DecisionTreeClassifier()
        #,ExtraTreeClassifier()
        #,LinearSVC()
        )
    print(clfr.Fit(usePipeLine=True, train_test_split_value=.20))
    print("Accurracy Scores: \n")
    d = clfr.getAccuracyScores()
    for k in d.keys():
        print("{}: {}\n".format(k, d.get(k)))
    
    tags = clfr.Predict([
        clfr.stemPhrase("harmful to the skin"),
        clfr.stemPhrase("Balloon Vine Extract"),
        clfr.stemPhrase("Blackcurrant Seed Oil")
        ])
    print(tags)
    return

def predictSentBinary():
    clfr = pickleutils.getPickledClassifier(SMBinaryNLTKClassifier.SMBinaryNLTKClassifier, SentenceSelections.UseSentence)
    ar = pickleutils.getPickledClassifier(SMPhraseAccuracyResult.SMPhraseAccuracyResult, SentenceSelections.UseSentence)
    sents = [
        "This product is used as skin lightening agents in the cosmetics, especially in advanced cosmetics which have function of lightening skin, sunscreen and dispelling freckle.",
        "This product may break down in the acidic or alkalic environment, so the pH value of cosmetic system should be between 6.5 and 7.5.",
        "It may be harmful to the skin when this product is compatible with other additives that have physiological effects, so the use of cosmetic formulations of this product should be fully studied.",
        "skin lightening agents in the cosmetics",
        "harmful to the skin",
        "Balloon Vine Extract",
        "Blackcurrant Seed Oil",
        "MossCellTecâ„¢ No. 1 has been developed from an extract of the cells of the Physcomitrella patens moss. It is the \
        first active ingredient on the market that is based on bio technologically produced moss which is obtained in \
        a reproducible and sustainable way by tissue culture. Mosses are among the first land plants to conquer the \
        earth. Their extremely high resilience to a changing environment makes them of considerable interest in regard to \
        fortifying our skin. "
        ]
    tags = clfr.Predict(sents)
    tagPrecisions = []
    for i, tag in enumerate(tags):
        tagPrecisions.append((tag, ar.CheckAccuracy(sents[i], tag)))
    print(tagPrecisions)
    return

def test_accuracy():
    ar = pickleutils.getPickledClassifier(SMPhraseAccuracyResult.SMPhraseAccuracyResult, SentenceSelections.UseSentence)
    sent = "It may be harmful to the skin when this product is compatible with other additives that have physiological effects, so the use of cosmetic formulations of this product should be fully studied"
    sent = "skin lightening agents in the cosmetics"
    sent = "This product is used as skin lightening agents in the cosmetics, especially in advanced cosmetics which have function of lightening skin, sunscreen and dispelling freckle"
    #phrase =  ['data', 'avail' ]
    logger.info("%s." % {'CLA': ar.CheckAccuracy(sent, 'CLA'), 'BEN': ar.CheckAccuracy(sent, 'BEN')})
    return

def testAutoTagger():
    from tools import SMAutomatedTagger
    import io, string
    # Open the estimater
    estimators = {
        #SentenceSelections.UseDocument : pickleutils.getPickledClassifier(SMBinaryNLTKClassifier.SMBinaryNLTKClassifier, SentenceSelections.UseDocument),
        #SentenceSelections.UseParagraph : pickleutils.getPickledClassifier(SMBinaryNLTKClassifier.SMBinaryNLTKClassifier, SentenceSelections.UseParagraph),
        SentenceSelections.UseParagraph : pickleutils.getPickledClassifier(SMDocumentClassifier.SMDocumentClassifier, SentenceSelections.UseParagraph),
        #SentenceSelections.UseSentence : pickleutils.getPickledClassifier(SMBinaryNLTKClassifier.SMBinaryNLTKClassifier, SentenceSelections.UseSentence),
        SentenceSelections.UseSentence : pickleutils.getPickledClassifier(SMDocumentClassifier.SMDocumentClassifier, SentenceSelections.UseSentence),
        SentenceSelections.UsePhrase : pickleutils.getPickledClassifier(SMDocumentClassifier.SMDocumentClassifier, SentenceSelections.UsePhrase),
    }
    accuracyCheckers = {
        #SentenceSelections.UseDocument : pickleutils.getPickledClassifier(SMPhraseAccuracyResult.SMPhraseAccuracyResult, SentenceSelections.UseDocument),
        SentenceSelections.UseParagraph : pickleutils.getPickledClassifier(SMPhraseAccuracyResult.SMPhraseAccuracyResult, SentenceSelections.UseParagraph),
        SentenceSelections.UseSentence : pickleutils.getPickledClassifier(SMPhraseAccuracyResult.SMPhraseAccuracyResult, SentenceSelections.UseSentence),
        SentenceSelections.UsePhrase : pickleutils.getPickledClassifier(SMPhraseAccuracyResult.SMPhraseAccuracyResult, SentenceSelections.UsePhrase),
        }
    inputFile = "./samples/Mibelle.txt"
    with SMAutomatedTagger.SMAutomatedTagger(inputFile, estimators, accuracyCheckers) as atagger:
        print("Domain: {0}.".format(atagger.getDomain()))
        inputFileName = os.path.splitext(os.path.basename(inputFile))[0]
        with open(os.path.join(os.path.dirname(inputFile), inputFileName + ".tagged.mlp.txt"), "w") as owriter:
            domTag = "\\" + '|'.join(atagger.getDomain()) + "["
            owriter.write(domTag)
            print("Paras:")
            paras = atagger.getTaggedParas()
            for i, para in enumerate(paras):
                tagAndPrecision, p = para
                tag, precision = tagAndPrecision
                sent = ''
                for s in p:
                    sent += "".join([" " + i if not i.startswith("'") and i not in string.punctuation else i for i in s]).strip()
                canbeTagged = len(sent) > 10 and precision >= .5
                logger.info("       {0}:{1}".format(tag, p))
                #if canbeTagged:
                owriter.write("\\%s(%.2f)[" % (tag, precision))
                owriter.write(sent)
                #if canbeTagged:
                owriter.write("\\]")
                owriter.write("\n")
            owriter.write("\\]")

            print("Sents:")
            with open(os.path.join(os.path.dirname(inputFile), inputFileName + ".sents.tagged.mlp.txt"), "w") as owriter:
                sents = atagger.getTaggedSents()
                for i, sent in enumerate(sents):
                    tagAndPrecision, s = sent
                    tag, precision = tagAndPrecision
                    logger.info("Found the tag as %s with accuracy %.4f for sent %s..." % (tag, precision, s[:50]))
                    owriter.write("\\%s(%.2f)[" % (tag, precision))
                    owriter.write(" ".join(s))
                    owriter.write("\\]")
                    owriter.write("\n")

            print("Phrases:")
            with open(os.path.join(os.path.dirname(inputFile), inputFileName + ".phrases.tagged.mlp.txt"), "w") as owriter:
                phrases = atagger.getTaggedPhrases()
                for i, phrase in enumerate(phrases):
                    tagAndPrecision, p = phrase
                    tag, precision = tagAndPrecision
                    logger.info("Found the tag as %s with accuracy %.4f for phrase %s..." % (tag, precision, p))
                    owriter.write("\\%s(%.2f)[" % (tag, precision))
                    owriter.write(p)
                    owriter.write("\\]")
                    owriter.write("\n")

    return

def PredictWithClusteredClassifier(sentence):
    tagset = DBSession.Create().getTags() # all tag definitions
    reader = getCurrentReader(BGConfig.CorpusLocation, tagset)
    clfcluster = ClassifierClusterWithScoring(SentenceSelections.UsePhrase, tagset)
    data = reader.Sents()
    data = list(map(list, zip(*data)))
    tags  = pd.Series(data=data[0])
    features = pd.Series(data=data[1])
    clfcluster.Fit(SentenceSelections.UseSentence, features, tags)
    logger.info(clfcluster.Predict(sentence))
    return


if __name__ == "__main__":
    #initSearch(recreateTrainingSets=True)
    #predictDocument()
    #predictSents()
    #predictPhrases()
    #predictSentBinary()
    #testAutoTagger()
    #test_accuracy()
    PredictWithClusteredClassifier("fr   Site certified according to ISO  9001, ISO  14001 and OHSAS 18001 standards")
