import nltk as nk
from .ClassifierMixin import  ClassifierMixin, SentenceSelections

class SMPhraseAccuracyResult(ClassifierMixin):
    """One method of figuring out the accuracy of the probability tag for any given sentence or phrase. 
    Improving Accuracy
    ------------------
    When a phrase is chosen, we need a specific way to report if
       a. Classification based on training set picks up a tag by certain percentile. This can be done probability based approach.

       Assume we have a collection of sets of words per tag
          TAG1 = { W11, W12, …., W1n }
          TAG2 = { W27, W29, …, W2n }
   
       This is just a set (order is not important).
   
       When we take a random new sentence, what we are doing is, trying to figure out which set (TAG1, TAG2, etc) matches closely with words in the new sentence. This is done by running through each word in the new phrase with each word in each of the tags. 
   
       Example. 
          Word1 in the phrase is checked in TAG1, then Word2, etc. Find how many of these words matched in TAG1
          Keep doing this against all the TAGS. 
          Find which TAG produced best occurrence rate (sum of all words in the new phrase).
      

    Once this is done, we have to an accuracy check using bigrams and trigrams (when order of the words matters).
    """

    __slots__ = [
        "_tagWords" # a dictionary of tag and word set pairs { "BEN" = {"W1", "W2" }, ... }
        ]

    def __init__(self, sel, features, tags):
        ''' Features and tags are pairs of sentences and tags '''
        ClassifierMixin.__init__(self, sel)
        self._tagWords = {}
        self._tagsToWordsSet(features, tags)

    def _tagsToWordsSet(self, features, tags):
        _temp__tagWords ={}
        for x, y  in zip(features, tags):
            x = super(SMPhraseAccuracyResult, self).stemPhrase(x)
            x1 = nk.wword_tokenize(x)
            if _temp__tagWords.get(y):
                _temp__tagWords[y].extend(x1)
            else:
                _temp__tagWords[y] = x1

        for x, y in _temp__tagWords.items():
            self._tagWords[x] = set(y)

        return self._tagWords


    def CheckAccuracy(self, phraseOrSent, tag = None, clean = True):
        """
        Check classification accuracy of the phrase. If tags contains tags, accuracy against thos tags is checked.
        Returns a number between 0.0 and 1.0

        1. cleanup
        2. stem
        sents = { w1, w2, ...}
        tags = ['BEN', 'CLA']
        for tag in tags:
            result = how many words (numerator) in sents (num of words in sents is denominator) is in tagwords.
        """
        if isinstance(phraseOrSent, list):
            phraseOrSent = " ".join(phraseOrSent)
        
        if not phraseOrSent:
            return 0.0

        if clean :
            phraseOrSent = self._tokenizeCleanandStemPhrase(phraseOrSent)
            if not phraseOrSent:
                return 0.0

        conditionalSet = set(nk.wword_tokenize(phraseOrSent))
        common_words = self._tagWords[tag].intersection(conditionalSet)
        accuracy_rate = len(common_words)/len(conditionalSet)
        return accuracy_rate
