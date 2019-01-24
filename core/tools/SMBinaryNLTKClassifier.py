import pandas as pd
import os, sys
import regex as rg
from . import SMEstimatorBase
from .ClassifierMixin import ClassifierMixin, SentenceSelections
import nltk
import io
import string

import pickle

class SMBinaryNLTKClassifier(SMEstimatorBase.SMEstimatorBase, ClassifierMixin):
    """Bayesian NLTK classifier WRAPPER
    """
    __slots__ = [
        "_uwordSet",
        "_classifier",
        "_test_set",
        "_features",
        "_targets"
        ]


    def __init__(self, selections, features = pd.Series(), targets = pd.Series()):
        '''
        Construct this instance. 
        @features: a list of sentences. When None, the class expects a locally picked trainingset.
        @targets: a list of tags. When None, the class expects a locally picked trainingset.
        Both features and targets are expected to be same size and tag of each sentences also 
        positioned at the same index.
        '''
        ClassifierMixin.__init__(self, selections)
        
        #if features.empty or targets.empty:
        #    if self.check_model():
        #        print ('Model loaded from  file ')
        #        f = open(self.get_file_name(), 'rb')
        #        self.classifier = pickle.load(f)
        #        f.close()
        #        return
        #    else:
        #        raise ValueError("Cannot find previously stored trainingset data. Please provide both features and targets arguments.")
        

        if not isinstance(features, pd.Series):
            raise ValueError("features is not a valid panda series")
        if not isinstance(targets, pd.Series):
            raise ValueError("targets is not a valid panda series")
        self._features = features
        self._targets = targets
        self._uwordSet = list(self.get_word_features())
        self._classifier = None
        return

    def get_word_features(self):
        word_set = set()
	    #TODO Stem words
        for x in self._features:
            for y in nltk.wword_tokenize(x.lower()):
                word_set.add(y)
        return word_set

    def document_features(self, document):
        features = {}
        for word in self._uwordSet:
            features[word] = 1 if word in document else 0
        return features

    def get_train_set_len(self):
        return int(len(self._features))

    def Fit(self, *, train_test_split_value = 0.0, usePipeLine=True):
        split_value = int(self.get_train_set_len() * train_test_split_value)
        featuresets = [(self.document_features(d), c) for (d, c) in zip(self._features, self._targets)]
        self._train_set, self._test_set = featuresets[split_value:], featuresets[:split_value]
        self._classifier = nltk.NaiveBayesClassifier.train(self._train_set)
        #if not self._classifier:
        #    self._classifier = nltk.NaiveBayesClassifier.train(self.train_set)
        #    f = open(self.get_file_name(), 'wb')
        #    pickle.dump(self.classifier, f)
        #    f.close()
        return None

    def getAccuracyScores(self):
        print(nltk.classify.accuracy(self._classifier, self._test_set))
        return self._classifier.show_most_informative_features(5)

    def Predict(self, newcontent):
        ''' Predict a new content. The new content can be either an "python list" of string contents or a string content'''
        if not self._classifier:
            self.Fit()
        if not newcontent:
            raise ValueError("newcontent must be a valid list of string contents or a single string content.")
        if not isinstance(newcontent, list):
            newcontent = [newcontent]
        newcontent = [ self.stemPhrase(self._clean_phrase(p)) for p in newcontent ]
        tags = [self._classifier.classify(self.document_features(ctnt)) for ctnt in newcontent]
        return tags

    def check_model(self):
        r = os.path.exists(os.path.join(".", self.get_file_name()))
        return r



