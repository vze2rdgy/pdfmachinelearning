import numpy as np
import pandas as pd
from .SMCorpusLineReader import SMCorpusLineReader 
from .ClassifierMixin import ClassifierMixin, SentenceSelections, ClassifyMethod
from sklearn.feature_extraction.text import * #CountVectorizer, HashingVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.preprocessing import *
from sklearn.naive_bayes import * #MultinomialNB
from sklearn.pipeline import * #Pipeline, make_pipeline
from sklearn.linear_model import *
from sklearn.model_selection import *
from sklearn import svm

class SMCorpusClassifier(ClassifierMixin):
    ''' Main corpus Classifier '''

    __slots__ = [
        '_reader', # SMCorpusReader instance.
        '_wordFactors', # A dictionary of word->uniquenumbers. Used for classifiers which only supports numerical values.
        '_bIsFitted',   # is the model fitted ?
        '_classifier', # bayes classifier
        ]

    def __init__(self, reader, selections = SentenceSelections.UseSentence, classifyMethod = ClassifyMethod.UseNone, useSynonyms = False):
        ''' Construct instance. 
        @p reader: An instance of SMCorpusReader.
        @p selections: One of the values in SentenceSelections enum. See ClassifierMixin.py
        '''
        self._wordFactors = None
        self._bIsFitted = False
        self._reader = reader
        super(SMCorpusClassifier, self).__init__(selections, classifyMethod, useSynonyms )
        if SentenceSelections.UseSentence == (selections & SentenceSelections.UseSentence) :
            self._buildDataframeAndFactorizeWords(self._reader.sents(), False)
        if SentenceSelections.UsePhrase == (selections & SentenceSelections.UsePhrase) :
            self._buildDataframeAndFactorizeWords(self._reader.phrases(), False)

    def getSelections(self):
        return super().getSelections()

    def Refit(self):
        _bIsFitted = False;

    def Fit(self):
        ''' Fit our corpus data to the model.'''
        if self._bIsFitted:
            return

        features = self._dataFrame['sent']
        targets = self._dataFrame['tag']
        targets = targets.astype('int')
        
        #self.count_vect = CountVectorizer()
        #x_train_count = self.count_vect.fit_transform(features)
        #tf_transformer = TfidfTransformer(use_idf=false).fit(x_train_count)
        #x_train_tf = tf_transformer.transform(x_train_count)
        #self.tfidf_transformer = TfidfTransformer()
        #x_train_tfidf = self.tfidf_transformer.fit_transform(x_train_count)
        #self._classifier = Perceptron(max_iter=1000, tol=1e-3).fit(x_train_tfidf, targets)
        
        #self._classifier = Pipeline([
        #        #('vect', HashingVectorizer()),
        #        #('tfidf', TfidfTransformer()),
        #        ('vect', TfidfVectorizer(
        #            sublinear_tf=True, max_df=0.5,
        #            stop_words='english')),
                #('clf1', svm.SVC(kernel='linear', C=1))
        #        #('clf0', MultinomialNB()),
        #        #('clf1', SGDClassifier(loss='perceptron', penalty='elasticnet', alpha=1e-3, random_state=42, max_iter=5, tol=None)),
        #        #('clf1', RidgeClassifier()),
        #        ('clf1', Perceptron(max_iter=1000, tol=1e-3)),
        #    ])

        self._classifier = Pipeline([
                ('vect', TfidfVectorizer(
                    sublinear_tf=True, max_df=0.5,
                    stop_words='english')),
                ('clf1', Perceptron(max_iter=1000, tol=1e-3)),
            ])
        
        if self.getSelections() == SentenceSelections.UseDocument or self.getSelections() == SentenceSelections.UseParagraph :
            # regular classifier fitting will work well for documents and paragraphs.
            self._classifier.fit(features, targets)
        elif self.getSelections() == SentenceSelections.UsePhrase or self.getSelections() == SentenceSelections.UseSentence:
            # for sentences and phrases, if we can fit with word stems or nouns, the match probability
            # will increase. If the prediction process can utilize permutations of synonyms, 
            # that will also increase the match probability.
            self._classifier.fit(features, targets)
        else:
            raise NotImplementedError('This type of phrase selections argument is not supported.')

        #from sklearn.model_selection import GridSearchCV
        #parameters = {
            #'vect__ngram_range': [(1, 1), (1, 2)],
            #'tfidf__use_idf': (True, False),
            #'clf__alpha': (1e-2, 1e-3),
        #}
        #self._classifier = GridSearchCV(self._classifier, parameters, n_jobs=-1)

        self._classifier = self._classifier.fit(features, targets)

        self._bIsFitted = True
        return

    def getCrossValidationScore(self):
        # cross validation check.
        if self._classifier :
            cv = ShuffleSplit(n_splits=3, test_size=0.3, random_state=0)
            cscore = cross_val_score(self._classifier, features, targets, cv=cv)
            print("Accuracy: %0.2f (+/- %0.2f)" % (cscore.mean(), cscore.std() * 2))
            return (cscore.mean(), cscore.std() * 2)
        raise RuntimeError('Classifier not defined.')

    def PredictSent(self, sent):
        ''' Pass a sentence and predict its tag type. '''
        return self.PredictSents([sent])

    def PredictSents(self, sents):
        ''' Pass a collection of sentences and predict their tags. 
            Returns a list of tags positioned at same index and the sent
            in sents list.
        '''
        if not self._bIsFitted:
            self.Fit()
        if not self._classifier:
            raise MemoryError('classifier is not initialized.')

        csents = self._cleanSents(sents)

        #X_new_counts = self.count_vect.transform(sents)
        #X_new_tfidf = self.tfidf_transformer.transform(X_new_counts)
        #predicted = self._classifier.predict(X_new_tfidf)

        # Not sure how to use score yet.
        #score = self._classifier.decision_function(sents)
        #print(score)

        if self.getSelections() == SentenceSelections.UseDocument or self.getSelections() == SentenceSelections.UseParagraph :
            # regular classifier fitting will work well for documents and paragraphs.
            predicted = self._classifier.predict(csents)
        elif self.getSelections() == SentenceSelections.UsePhrase or self.getSelections() == SentenceSelections.UseSentence:
            # for predicting matching sentences and phrases, we will need permutations of synonyms and also
            # possibly each word in the sentence/phrase converted to its stems or nouns. 
            # for stems and nouns, we the fitting process also must follow the same mechanism
            # before creating confusion matrix based on word frequency.

            if super().getUseSynonyms() :
                for sent in csents:
                    sentPermuts = super().generatePhrasePermutations(sent)
                    if sentPermuts :
                        sentPermuts.head()

            predicted = self._classifier.predict(csents)

        else:
            raise NotImplementedError('This type of phrase selections argument is not supported.')

        return [self._reader._tagset._uniqids.get(p) for p in predicted]



