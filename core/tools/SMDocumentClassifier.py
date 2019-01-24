from . import SMEstimatorBase
from .ClassifierMixin import ClassifierMixin, SentenceSelections
import pandas as pd
from sklearn.feature_extraction.text import * #CountVectorizer, HashingVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.pipeline import * #Pipeline, make_pipeline
from sklearn.linear_model import *
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, hamming_loss, matthews_corrcoef #balanced_accuracy_score
from sklearn.neural_network import MLPClassifier

class SMDocumentClassifier(SMEstimatorBase.SMEstimatorBase, ClassifierMixin):
    """
    Accepts a pair of pd.Series of document elements (doc contents and doc tag)
    The doc contents series is used as sample features and doc tag series is used
    as sample targets.

    Using them, constructs a training set by fitting into a sklearn classifier.

    The Predict method then can be used to input a random new content and obtain 
    corresponding document tag.
    """

    __slots__ = [
        "_series_contents",
        "_series_tags",
        "_classifier_algo",
        "_classifier",
        "_lastytest",
        "_lastypred"
        ]

    def __init__(self, sel, series_contents = None, series_tags = None, classifier_algo = None):
        if not isinstance(series_contents, pd.Series):
            raise ValueError("series_contents is not a valid panda series")
        if not isinstance(series_contents, pd.Series):
            raise ValueError("series_tags is not a valid panda series")
        ClassifierMixin.__init__(self, sel)
        self._series_contents = series_contents
        self._series_tags = series_tags
        self._classifier_algo = classifier_algo
        self._lastytest = None
        self._lastypred = None
        return

    def Fit(self, *, train_test_split_value = 0.0, usePipeLine=True):
        ''' Fit with classifier and obtain a classification scoring report of the form
        {'label 1': {'precision':0.5,
             'recall':1.0,
             'f1-score':0.67,
             'support':1},
        'label 2': { ... },
          ...
        }'''

        x_train, x_test, y_train, self._lastytest = train_test_split(
            self._series_contents, self._series_tags, 
            test_size=train_test_split_value, random_state=42,
            shuffle=False
            )

        if usePipeLine:
            vect = TfidfVectorizer(
                sublinear_tf=True, max_df=0.5,
                stop_words='english')
            transformed = vect.fit_transform(x_train)
            shape = transformed.shape
            if isinstance(self._classifier_algo, MLPClassifier):
                numOfHiddenLayers = int(1/2 * (shape[1] - y_train.shape[0]))
                params = self._classifier_algo.get_params()
                self._classifier_algo.set_params(hidden_layer_sizes=(numOfHiddenLayers,))
            self._classifier = Pipeline([
                    ('vect', vect),
                    ('clf1', self._classifier_algo),
                ])
        else:
            self._classifier = self._classifier_algo

        self._classifier.fit(x_train, y_train)

        if not train_test_split_value:
            return None
        # check accuracy
        self._lastypred = self._classifier.predict(x_test)
        ''' The classification report returns below info:
            precision: tp / (tp + fp) => tp = true positives, fp = false positives. 
                Ability of classifier not to label as positive a sample that is negative
            recall: tp / (tp + fn) => fn = false negatives. 
                Ability of classifier to find positive samples
            f1-score: f-beta score is weighted harmonic mean of precision and recall. 
                Best score = 1.0 and worst score = 0.0 
            support: number of occurrences of each class in y_true

        '''
        return classification_report(self._lastytest, self._lastypred)

    def getAccuracyScores(self):
        if not len(self._lastytest):
            return {}
        return {
            "subset accuracy" : accuracy_score(self._lastytest, self._lastypred),
            #"average of recall obtained on each class" : balanced_accuracy_score(self._lastytest, self._lastypred),
            "fraction of labels that are incorrectly predicted" : hamming_loss(self._lastytest, self._lastypred),
            #"measure of the quality of binary and multiclass classifications" : matthews_corrcoef(self._lastytest, self._lastypred)
            }



    def Predict(self, newcontent):
        ''' Predict a new content. The new content can be either an "python list" of string contents or a string content'''
        if not self._classifier:
            self.Fit()
        if not newcontent:
            raise ValueError("newcontent must be a valid list of string contents or a single string content.")
        if not isinstance(newcontent, list):
            newcontent = [newcontent]
        newcontent = [ self.stemPhrase(self._clean_phrase(p)) for p in newcontent ]
        return self._classifier.predict(newcontent)









