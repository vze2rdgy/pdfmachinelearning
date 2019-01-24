import sys
import os
import nltk as nk
import nltk.corpus.reader.plaintext as ptxt
from . import SMDocumentClassifier
from . import SMPhraseAccuracyResult
from .ClassifierMixin import ClassifierMixin, SentenceSelections
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class SMAutomatedTagger(ClassifierMixin):
    """
    The class accepts a text document and attempts to tag
    every sentence and phrases in the document with tags
    which has highest probability match based on trained classifiers.
    And in the end, it will also classify the document's domain.

    In future, it will also attempt to mark offsets in the original 
    document (pdf, etc) where the tags are placed. 
    (tag : (distance offset from the start of document, sentence/phrase length, page number))

    """
    __slots__ = [
        "_reader",
        "_ests",
        "_acrcheckrs",
        "_logger",
        "_stemmer"
        ]

    def __init__(self, newfilePath, estimators, accuracyCheckers = None):
        """
           Attempt to automatically tag a document. While tagging, the 
           offset, respective length and page number of tagged sections 
           of the document will be recorded in an array.
           @newfilepath:  A new file which is going to be tagged. This file is in text format.
           @estimators: A dictionary of SentenceSelections : EstimatorBase
        """
        ClassifierMixin.__init__(self, SentenceSelections.UseDocument)
        self._stemmer = None
        self._logger = logging.getLogger('tools.SMAutomattedTagger')
        self._logger.setLevel(logging.INFO)
        self._ests = estimators
        self._acrcheckrs = accuracyCheckers
        self._reader = ptxt.PlaintextCorpusReader(os.path.dirname(newfilePath), [os.path.basename(newfilePath)], encoding='iso-8859-15') #encoding='iso-8859-15'
        return

    def __enter__(self):
        """ Open the file and start auto tagging """
        self.beginTagging()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Finish with tagging and close the file."""
        try:
            if exc_value:
                print(exc_value)
                print(traceback)
            self.Close()
        except Exception:
            print(sys.exc_info())
            print(sys.exc_traceback())
        return True

    def beginTagging(self):
        #encoding = self._reader.encoding(self._reader.fileids()[0])
        #if SentenceSelections.UseDocument in self._ests:
        #    self._tagDomain()
        #if SentenceSelections.UseParagraph in self._ests:
        #    self._tagParas()
        #if SentenceSelections.UseSentence in self._ests:
        #    self._tagSents()
        #if SentenceSelections.UsePhrase in self._ests:
        #    self._tagPhrases()
        return

    def _cleanupWords(self, words):
        ''' 
        Remove from the words array, stop words and punctuations and stem the words. 
        return the resulting array.
        '''
        import nltk.stem as stems
        import string
        if not self._stemmer:
            self._stemmer = stems.porter.PorterStemmer()
        rwords = []
        if not self._engstopwords:
            self._engstopwords = spw.words('english')
        for w in words:
            w = w.strip().lower()
            if w in string.punctuation:
                continue
            if w in self._engstopwords:
                continue
            w = self._stemmer.stem(w)
            rwords.append(w)
        return rwords

    def _tagDomain(self):
        ''' Experimental: Tags the whole document with domain tag. '''
        clfr = self._ests.get(SentenceSelections.UseDocument)
        if not clfr :
            return 'NON'
        words = self._reader.words()
        # clean up and stem
        words = self._cleanupWords(words)
        content = ' '.join(words)
        self._logger.info("Finding Domain....")
        domain = clfr.Predict(content)
        self._logger.info("Found the domain as %s." % domain)
        return domain

    #def _unifiedTagging(self):
    #    ''' Experimental: Tags the given paragraph with its tag. '''
    #    #IMPORTANT: Since paras already contains sentences and phrases, 
    #    # tagging sentence and phrases will take place here itself.

    #    paras = self._reader.paras()
    #    rparas = []
    #    for p in paras:
    #        para = ""
    #        for s in p:
    #            s = self._cleanupWords(s)
    #            para += " ".join(s)
    #        rparas.append((para, p))

    #    # classify
    #    prest = None # paragraph estimators
    #    sentest = None # sentence estimators
    #    phest = None # phrase estimators
    #    prac= None # paragraph accuracy checker
    #    sentac= None # sentence accuracy checker
    #    phac= None # phrase accuracy checker

    #    if SentenceSelections.UseParagraph in self._ests:
    #        prest = self._ests[SentenceSelections.UseSentence]
    #    if SentenceSelections.UseSentence in self._ests:
    #        sentest = self._ests[SentenceSelections.UseSentence]
    #    if SentenceSelections.UsePhrase in self._ests:
    #        phest = self._ests[SentenceSelections.UsePhrase]
        
    #    if SentenceSelections.UseParagraph in self._acrcheckrs:
    #        prac = self._acrcheckrs[SentenceSelections.UseSentence]
    #    if SentenceSelections.UseSentence in self._acrcheckrs:
    #        sentac = self._acrcheckrs[SentenceSelections.UseSentence]
    #    if SentenceSelections.UsePhrase in self._acrcheckrs:
    #        phac = self._acrcheckrs[SentenceSelections.UsePhrase]

    #    taggedParas = []
    #    taggedSents = []
    #    taggedPhrases = []
    #    self._logger.info("Classifying paragraphs....")
    #    for pcleaned, porig in rparas:
    #        if prest:
    #            tag = ['NON'] if not pcleaned else prest.Predict(pcleaned)
    #            if tag :
    #                tag = tag[0]
    #            if 'NON' in tag: continue
    #            verify = 1.0
    #            if prac:
    #                verify = prac.CheckAccuracy(pcleaned, tag)
    #            taggedParas.append(((tag, verify), porig))
    #        self._logger.info("Found the tag as %s with accuracy %.4f for paragraph %s..." % (tag, verify, porig[:50]))
    #    self._taggedParas = taggedParas

    def _tagParas(self):
        ''' Experimental: Tags the given paragraph with its tag. '''
        #IMPORTANT: Since paras already contains sentences and phrases, 
        # tagging sentence and phrases will take place here itself.
        prest = self._ests.get(SentenceSelections.UseParagraph)
        if not prest:
            return []

        paras = self._reader.paras()
        rparas = []
        for p in paras:
            para = ""
            for s in p:
                s = self._cleanupWords(s)
                para += " ".join(s)
            rparas.append((para, p))

        # classify
        prac = self._acrcheckrs.get(SentenceSelections.UseParagraph)
        self._logger.info("Classifying paragraphs....")
        for pcleaned, porig in rparas:
            tag = ['NON'] if not pcleaned else prest.Predict(pcleaned)
            if tag :
                tag = tag[0]
            if 'NON' in tag: continue
            verify = 1.0
            if prac:
                verify = prac.CheckAccuracy(pcleaned, tag, False)
            else:
                verity = 0.0
            yield ((tag, verify), porig)
        return []

    def _tagSents(self):
        ''' Experimental: Tags the given sentence with its tag. '''
        est = self._ests.get(SentenceSelections.UseSentence)
        if not est:
            return []
        achecker = self._acrcheckrs.get(SentenceSelections.UseSentence)
        sents = self._reader.sents()
        for origSent in sents:
            cleanedSent = ' '.join(self._cleanupWords(origSent))
            tag = ['NON'] if not cleanedSent else est.Predict(cleanedSent)
            if tag:
                tag = tag[0]
            if 'NON' in tag: continue
            verify = 1.0
            if achecker:
                verify = achecker.CheckAccuracy(cleanedSent, tag, False)
            else:
                verity = 0.0
            yield ((tag, verify), origSent)
        return []

    def _tagSent(self):
        ''' Experimental: Tags the given sentence with its tag. '''
        pass

    def _tagPhrases(self):
        ''' Experimental: Tags the given phrase with its tag. '''
        # use trigrams http://www.nltk.org/howto/collocations.html
        est = self._ests.get(SentenceSelections.UsePhrase)
        if not est:
            return []

        achecker = self._acrcheckrs.get(SentenceSelections.UsePhrase)
        sents = self._reader.sents()
        #for sentence in sents:
        #    print(sentence)
        #    #print(sentence)
        #    bigrams = self.get_ngrams(' '.join(sentence), 2)
        #    for origSent in bigrams:
        #        cleanedSent = ' '.join(self._cleanupWords([origSent]))
        #        tag = ['NON'] if not cleanedSent else est.Predict(cleanedSent)
        #        if tag:
        #            tag = tag[0]
        #        if 'NON' in tag: continue
        #        verify = 1.0
        #        if achecker:
        #            verify = achecker.CheckAccuracy(cleanedSent, tag, False)
        #        self._taggedPhrases.append(((tag, verify), origSent))
        #        #print(origSent)
        for sentence in sents:
            trigrams = self.get_ngrams(' '.join(sentence), 3)
            for tgram in trigrams:
                cleanedSent = ' '.join(self._cleanupWords(ClassifierMixin.wordTokenize(tgram)))
                tag = ['NON'] if not cleanedSent else est.Predict(cleanedSent)
                if tag:
                    tag = tag[0]
                if 'NON' in tag: continue
                verify = 1.0
                if achecker:
                    verify = achecker.CheckAccuracy(cleanedSent, tag, False)
                else:
                    verity = 0.0
                yield ((tag, verify), tgram)
        return []

    def _tagPhrase(self):
        ''' Experimental: Tags the given phrase with its tag. '''
        pass

    def _reconstitute(self):
        '''Experimental: Reconstructs the file after its contents are tagged. '''
        pass

    def Close(self):
        """Finish with tagging and close the file and other resources"""
        pass

    def getDomain(self):
        return self._tagDomain()

    def getTaggedParas(self):
        return self._tagParas()

    def getTaggedSents(self):
        return self._tagSents()

    def getTaggedPhrases(self):
        return self._tagPhrases()




