import string
import sklearn as sk
from enum import *
import nltk as nk
from nltk.corpus import stopwords as spw
import pandas as pd
from nltk.collocations import *
from nltk.corpus import wordnet as wn
from . import TagSet
import regex as rg
#from nltk.tokenize import word_tokenize
from nltk.util import ngrams


class SentenceSelections(Enum):
    UseSentence = 1
    UsePhrase = 2
    UseParagraph = 4
    UseDocument = 8

class ClassifyMethod(Enum):
    UseNone = 0
    UseWordStems = 1
    UseWordNouns = 2

class ClassifierMixin(object):
    ''' A mixin class that contains functions
        that provides utility functions for 
        standard machine learning learning classifiers.
    '''
    __slots__ = [
        '_tagset',          # Tags that identifies phrases in pharmaceutical sense.
        '_begintagpattern', # The regex pattern of our special begin tag  
        '_endtagpattern',   # The regex pattern for our special end tag
        #'_repattern',   # patterns that includes tags and contents
        '_rgtags',      # compiled version of regex which gets tagged data.
        #'_resubpatt',       # Regex pattern to replace tags from the sentence or phrase.
        '_rgrepltags',       # compiled regex pattern to remove tags 
        '_dataFrame', # Sentence to Tags relation list.
        '_engstopwords', # english stop words
        '_selections',   # SentenceSelections enum value.
        '_bigramMeasures', # For bigram measuring
        '_trigramMeasures', # for trigram measuring
        '_classifyMethod',
        '_useSynonyms',
        '_wordFactors',
        '_pickledName',
        '_stemmer'
       ]

    def __init__(self, selections, tags, classifyMethod = ClassifyMethod.UseNone, useSynonyms = False):
        self._tagset = tags
        self._begintagpattern = r'\\[A-Za-z]{3}\['    # TODO: if not used remove these two variables
        self._endtagpattern = '\\\]' # TODO: if not used remove these two variables
        #self._repattern = r'(\\[A-Z]{3}\[)(.*)(\\\])'
        #self._resubpatt = r'(\\[A-Z]{3}\[)|(\\\])'
        self._selections = selections
        self._classifyMethod = classifyMethod
        self._useSynonyms = useSynonyms
        self._dataFrame = pd.DataFrame(columns=['sent', 'tag'])
        self._engstopwords = spw.words('english')
        self._wordFactors = {}
        self._bigramMeasures = None
        self._trigramMeasures = None
        self._rgtags = rg.compile(r'(\\[A-Za-z]{3}\[)(.*)(\\\])', rg.IGNORECASE | rg.MULTILINE)
        self._rgrepltags = rg.compile(r'(\\[A-Za-z]{3}\[)|(\\\])', rg.IGNORECASE | rg.MULTILINE)
        self._pickledName = None
        self._stemmer = None
        return 

    def get_file_name(self):
        if not self._pickledName :
            self._pickledName = str(type(self).__name__) + str(self._selections) + '.pickle'
        return self._pickledName

    def TagsInfo(self):
        return self._tagset

    def getSelections(self):
        return self._selections

    def getClassifyMethod(self):
        return self._classifyMethod

    def getUseSynonyms(self):
        return self._useSynonyms

    @staticmethod
    def wordTokenize(phrase):
        if phrase:
            #return nk.word_tokenize(phrase)
            return phrase.split()
        return phrase

    def _clean_phrase(self, phrase):
        ''' Remove tags embedded in the sentence. '''
        ph = self._rgrepltags.sub('', phrase)
        if not self._engstopwords:
            self._engstopwords = spw.words('english')
        cleaned = ''
        for w in ClassifierMixin.wordTokenize(phrase): #ph.split():
            w = w.strip().lower()
            if w in string.punctuation:
                continue
            if w not in self._engstopwords:
                cleaned += w
                cleaned += ' '
        cleaned = cleaned.strip()
        return cleaned

    def _tokenizeCleanandStemPhrase(self, phrase):
        import nltk.stem as stems
        if not self._stemmer:
            self._stemmer = stems.porter.PorterStemmer()
        toks = wordTokenize(phrase)
        #toks = phrase.split()
        if not self._engstopwords:
            self._engstopwords = spw.words('english')
        rwords = []
        for w in toks:
            w = w.strip().lower()
            if w in string.punctuation:
                continue
            if w in self._engstopwords:
                continue
            w = self._stemmer.stem(w)
            rwords.append(w)
        return rwords

    def _buildDataframeAndFactorizeWords(self, worddata, cleansent):
        ''' Internally builds and dataframe from sentences or phrases.
            The dataframe has columns of their tag and sent/phrase.
            The sentences/phrases are cleaned from stopwords and punctuations.
        '''
        sents = worddata
        if sents:
            idx = 0
            for k,v in sents.items():
                for s in v:
                    cleaned = ''
                    for w in wordTokenize(s): # s.split():
                        w = w.strip().lower()
                        if w in string.punctuation:
                            continue
                        if cleansent and w not in self._engstopwords:
                            #TODO: convert word to its noun form for analysis stability.
                            cleaned += w
                        else:
                            cleaned += w
                        cleaned += ' '
                        factor = self._wordFactors.get(w)
                        if factor:
                            factor = [factor[0], factor[1] + 1]
                        else:
                            factor = [len(self._wordFactors), 1]
                        self._wordFactors[w] = factor
                    self._dataFrame.loc[idx]=[cleaned.strip(), self._reader._tagset._tagtoids[k.strip()]]
                    idx += 1

    def _cleanSents(self, sents):
        ''' Remove stopwords and punctuations from the given list of sentences.'''
        if not self._engstopwords:
            self._engstopwords = spw.words('english')
        r = []
        for sent in sents:
            cleaned = ''
            for w in wordTokenize(sent): # sent.split():
                w = w.strip().lower()
                if w in string.punctuation:
                    continue
                if w not in self._engstopwords:
                    cleaned += w
                    cleaned += ' '
            cleaned = cleaned.strip()
            r.append(cleaned)
        return r

    def generatePhrasePermutations(self, phraseorsent):
        ''' 
           Call this method with a sentence or a phrase and 
           generate a new list of sentences replacing
           each word with their possible synonyms.
           Note: if there are units or measurements like
           3%, multiple sentences/phrases will be generated such that
           3%, 3 %, 3 pct, 3 percentage, 3 percent, etc will be included.
        '''
        raise NotImplementedError()
        words = wordTokenize(phraseorsent)
        dwords = dict()
        for i, w in enumerate(words):
            # add column    
            colName = 'w{0}'.format(i)
            if w not in dwords:
                dwords[colName] = [w]
            else:
                dwords[colName].append(w)
            #build permutations of the sentence using all good synonyms
            # replace underscore in the synonym word with a space.
            syns = self.getSynonyms(w)
            for w in syns:
                w = w.replace('_', ' ')
                dwords[colName].append(w)
        df = pd.DataFrame()

        return df

    def getSynonyms(self, word):
        ''' 
        Return synonyms of the given word.
        see: http://www.nltk.org/howto/wordnet.html
        Yield return was more efficient, but we need a way
        to prevent duplicates.
        '''
        synonyms = set()
        for n in wn.synsets(word, lang='eng'):
            for h in n.hypernyms():
                for syn in h.lemma_names():
                    synonyms.add(syn)
        return synonyms

    def getBigrams(self, sent):
        ''' 
        Get a list of bigrams from the given sentence.
        see: http://www.nltk.org/howto/collocations.html
        eg: 
         [('Enhances', 'cell'),
         ('cell', 'nucleus'),
         ('for', 'resilient'),
         ('function', 'for'),
         ('nucleus', 'function'),
         ('resilient', 'skin')]
        '''
        if not self._bigramMeasures:
            self._bigramMeasures = BigramAssocMeasures()
        finder = BigramCollocationFinder.from_words(wordTokenize(sent))
        #finder = BigramCollocationFinder.from_words(sent.split())
        return finder.nbest(self._bigramMeasures.pmi, 10)  # doctest: +NORMALIZE_WHITESPACE

    def getTrigrams(self, sent):
        ''' 
        Get a list of trigrams from the given sentence.
        see: http://www.nltk.org/howto/collocations.html
        eg 
        [('Refines', 'skin', 'and'),
         ('a', 'flawless', 'complexion'),
         ('and', 'creates', 'a'),
         ('creates', 'a', 'flawless'),
         ('skin', 'and', 'creates')]
        '''
        if not self._trigramMeasures :
            self._trigramMeasures = TrigramAssocMeasures()
        #finder = TrigramCollocationFinder.from_words(wordTokenize(sent))
        finder = TrigramCollocationFinder.from_words(sent.split())
        return finder.nbest(self._trigramMeasures.pmi, 10)  # doctest: +NORMALIZE_WHITESPACE

    def stemPhrase(self, sentorphrase, stemmer = 'porter'):
        ''' 
        Stemming is the process of removing morphological affixes from each
        word in a phrase or sentence. Eg. Enhances => Enhanc, nucleus => nucleu
        This is useful when you want to train a dataset without being concerned
        about a word's different forms (presentense, pastense, noun, etc.)
        see: http://www.nltk.org/howto/stem.html
        '''
        import nltk.stem as stems
        if not self._stemmer:
            if stemmer == 'porter':
                self._stemmer = stems.porter.PorterStemmer()
            else:
                self._stemmer = stems.snowball.SnowballStemmer("english")
        newphrase = ''
        #toks = wordTokenize(sentorphrase)
        #toks1 = sentorphrase.split()
        for w in ClassifierMixin.wordTokenize(sentorphrase):
            newphrase += self._stemmer.stem(w)
            newphrase += ' '
        return newphrase.rstrip()

    def nounifyPhrase(self, sentorphrase):
        ''' 
        Convert each word in a phrase or sentence to its noun form.
        '''
        raise NotImplementedError()

    def get_ngrams(self, text, n):
        if isinstance(text, list):
            text = " ".join(text)
        n_grams = ngrams(word_tokenize(text), n) 
        for grams in n_grams:
            yield ' '.join(grams)


#if __name__ == "__main__":
#    print('testing')
#    a = ClassifierMixin(SentenceSelections.UseDocument)
#    text = 'All 19 Black Women Running for Judge in a Texas Race Won Last Night'
#    print(a.get_ngrams(text, 2))
#    print(a.get_ngrams(text, 3))