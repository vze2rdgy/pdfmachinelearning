import os
from . import BGConfig
import logging
from sklearn.linear_model import PassiveAggressiveClassifier, SGDClassifier, RidgeClassifier
from sklearn.svm import LinearSVC
from sklearn.naive_bayes import MultinomialNB
from .tools import ComplementNB
from .tools.ClassifierMixin import ClassifierMixin, SentenceSelections, ClassifyMethod
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
from .tools.SMCorpusDocumentReader import SMCorpusDocumentReader
from .utils import pickleutils
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import Perceptron
from sklearn.tree import DecisionTreeClassifier

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

"""
ComplementNB(alpha=0.1, class_prior=None, fit_prior=True, norm=False) :         accuracy:   0.911

Passive-Aggressive                                                             
PassiveAggressiveClassifier(C=1.0, average=False, class_weight=None,
              fit_intercept=True, loss='hinge', max_iter=50, n_iter=None,
              n_jobs=1, random_state=None, shuffle=True, tol=0.001,
              verbose=0, warm_start=False):                                     accuracy:   0.904

SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', max_iter=50, n_iter=None,
       n_jobs=1, penalty='l2', power_t=0.5, random_state=None,
       shuffle=True, tol=None, verbose=0, warm_start=False):                    accuracy:   0.902

L2 penalty:
LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.001,
     verbose=0):                                                                accuracy:   0.900

Elastic-Net penalty
SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', max_iter=50, n_iter=None,
       n_jobs=1, penalty='elasticnet', power_t=0.5, random_state=None,
       shuffle=True, tol=None, verbose=0, warm_start=False):                    accuracy:   0.900

Naive Bayes:
MultinomialNB(alpha=0.01, class_prior=None, fit_prior=True):                    accuracy:   0.899

Ridge Classifier
RidgeClassifier(alpha=1.0, class_weight=None, copy_X=True, fit_intercept=True,
        max_iter=None, normalize=False, random_state=None, solver='sag',
        tol=0.01):                                                              accuracy:   0.897

SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
       eta0=0.0, fit_intercept=True, l1_ratio=0.15,
       learning_rate='optimal', loss='hinge', max_iter=50, n_iter=None,
       n_jobs=1, penalty='l1', power_t=0.5, random_state=None,
       shuffle=True, tol=None, verbose=0, warm_start=False):                    accuracy:   0.886

BernoulliNB(alpha=0.01, binarize=0.0, class_prior=None, fit_prior=True):        accuracy:   0.884

LinearSVC with L1-based feature selection
Pipeline(memory=None,
     steps=[('feature_selection', SelectFromModel(estimator=LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l1', random_state=None, tol=0.001,
     verbose=0),
        norm_order=1, prefit=...ax_iter=1000,
     multi_class='ovr', penalty='l2', random_state=None, tol=0.0001,
     verbose=0))]):                                                             accuracy:   0.880

Perceptron
Perceptron(alpha=0.0001, class_weight=None, eta0=1.0, fit_intercept=True,
      max_iter=50, n_iter=None, n_jobs=1, penalty=None, random_state=0,
      shuffle=True, tol=0.001, verbose=0, warm_start=False):                    accuracy:   0.881

L1 penalty
LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
     intercept_scaling=1, loss='squared_hinge', max_iter=1000,
     multi_class='ovr', penalty='l1', random_state=None, tol=0.001,
     verbose=0):                                                                accuracy:   0.873

kNN
KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
           metric_params=None, n_jobs=1, n_neighbors=10, p=2,
           weights='uniform')                                                   accuracy:   0.858

NearestCentroid (aka Rocchio classifier):                                       
NearestCentroid(metric='euclidean', shrink_threshold=None):                     accuracy:   0.855

Random forest
RandomForestClassifier(bootstrap=True, class_weight=None, criterion='gini',
            max_depth=None, max_features='auto', max_leaf_nodes=None,
            min_impurity_decrease=0.0, min_impurity_split=None,
            min_samples_leaf=1, min_samples_split=2,
            min_weight_fraction_leaf=0.0, n_estimators=100, n_jobs=1,
            oob_score=False, random_state=None, verbose=0,
            warm_start=False):                                                  accuracy:   0.834


"""


##TODO remove sents and tags. Only used for testing purpose.
#sents = [
#'safe nightli use skin type , includ sensit skin',
#'virgin marula oil : high critic antioxid omega 6 9 , nourish oil boost cleans makeup-remov power',
#'10 % serilisene® help increas skin elast',
#'mitracarpu scaber extract',
#'improv visibl sign age',
#'salicyl acid ( bha ) help chemic exfoli skin\x92 surfac improv appear problem skin',
#'nourish facial oil hydrat smooth skin type',
#'zinc pca asia',
#'banana signific amount fructos',
#'recommend level use 3 %',
#'srebp-1 ( sterol regulatori element-bind protein ) mrna express human adipocyt',
#'appear white',
#'90 % saw eye puffi reduc within 4 hours* use eye serum target four sourc puffi',
#'gardenia cell extract help target skin\x92 natur collagen',
#'immedi transform silki emuls water ad , rins perfectli clean oil residu',
#'94 % found skin healthi glow',
#'cucumi melo cantalupensi ( cantaloup ) fruit extract : rich antioxid , help sooth hydrat',
#'vehicl : butylen glycol , water',
#'hog plum , jamaica call spanish plum gulli plum . cajã¡ plant rich vitamin a , b1 , b2 , c , calcium , iron phosphoru . cajã¡ refer anti-inflammatori tradit medicin , use adstring , emet , stomachach',
#'color ( 3 % solut , apha ) 70 max',
#]

#tags = [
#    'CLA',
#    'CLA',
#    'NUM',
#    'INC',
#    'CLA',
#    'CLA',
#    'CLA',
#    'ORI',
#    'CMN',
#    'USL',
#    'MSR',
#    'PRO',
#    'NUM',
#    'CLA',
#    'CLA',
#    'NUM',
#    'CLA',
#    'ECA',
#    'CMN',
#    'PRO'
#]


class ClassifierClusterWithScoring(ClassifierMixin):
    """ 
    A collection of classifiers used for classification purpose.
    Multiple classifiers are used for training and prediction and
    the results are tagged dominance of prediciton results.
    Example if there are 5 classifiers and 3 of them predicted a value
    and others predicted something else, the most predicted value is
    selected as the tag.
    If all classifiers predicted different values, the result is rejected.
    """

    __slots__ = [
        '_classifierList',
        '_countVectorizer',
        '_tfidTransformer',
        '_tfidf_transformed',
        '_currentSelection'
        ]


    def __init__(self, sel, tags):
        ClassifierMixin.__init__(self, sel, tags, ClassifyMethod.UseNone, False )
        self._classifierList = [
            ComplementNB.ComplementNB(alpha=0.1, class_prior=None, fit_prior=True, norm=False),
            PassiveAggressiveClassifier(C=1.0, average=False, class_weight=None,
                          fit_intercept=True, loss='hinge', max_iter=50, n_iter=None,
                          n_jobs=1, random_state=None, shuffle=True, tol=0.001,
                          verbose=0, warm_start=False),
            SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
                   eta0=0.0, fit_intercept=True, l1_ratio=0.15,
                   learning_rate='optimal', loss='hinge', max_iter=50, n_iter=None,
                   n_jobs=1, penalty='l2', power_t=0.5, random_state=None,
                   shuffle=True, tol=None, verbose=0, warm_start=False),
            LinearSVC(C=1.0, class_weight=None, dual=False, fit_intercept=True,
                 intercept_scaling=1, loss='squared_hinge', max_iter=1000,
                 multi_class='ovr', penalty='l2', random_state=None, tol=0.001,
                 verbose=0),
            SGDClassifier(alpha=0.0001, average=False, class_weight=None, epsilon=0.1,
                   eta0=0.0, fit_intercept=True, l1_ratio=0.15,
                   learning_rate='optimal', loss='hinge', max_iter=50, n_iter=None,
                   n_jobs=1, penalty='elasticnet', power_t=0.5, random_state=None,
                   shuffle=True, tol=None, verbose=0, warm_start=False),
            MultinomialNB(alpha=0.01, class_prior=None, fit_prior=True),
            RidgeClassifier(alpha=1.0, class_weight=None, copy_X=True, fit_intercept=True,
                    max_iter=None, normalize=False, random_state=None, solver='sag',
                    tol=0.01),
            Perceptron(alpha=0.0001, class_weight=None, eta0=1.0, fit_intercept=True,
                    max_iter=50, n_iter=None, n_jobs=1, penalty=None, random_state=0,
                    shuffle=True, tol=0.001, verbose=0, warm_start=False),
            KNeighborsClassifier(algorithm='auto', leaf_size=30, metric='minkowski',
                    metric_params=None, n_jobs=1, n_neighbors=10, p=2,
                    weights='uniform'),
            DecisionTreeClassifier()
        ]

    @classmethod
    def Unpickle(cls, sel):
        if not os.path.exists(BGConfig.PickledClassifiers):
            logger.warn("There are no pickled classifiers")
            return None
        return pickleutils.getPickledClassifier(cls.__name__, sel, BGConfig.PickledClassifiers)

    @classmethod
    def Pickle(cls, instance):
        if not os.path.exists(BGConfig.PickledClassifiers):
            os.makedirs(BGConfig.PickledClassifiers)
        pickleutils.pickleClassifier(instance, BGConfig.PickledClassifiers)
        return

    @classmethod
    def IsPickled(cls, sel):
        return pickleutils.isPickled(cls.__name__, sel, BGConfig.PickledClassifiers)

    def _train(self):
        pass

    def Fit(self, sel, features, tags, testsize=0.0):
        self._currentSelection = sel
        # count vectorizer
        self._countVectorizer = CountVectorizer()
        X_train_counts = self._countVectorizer.fit_transform(features)
        self._tfidTransformer = TfidfTransformer()
        self._tfidf_transformed = self._tfidTransformer.fit_transform(X_train_counts)
        for clf in self._classifierList:
            clf.fit(self._tfidf_transformed, tags)
        return True

    def Predict(self, newcontent, bestTag = False):
        newcontent = self.stemPhrase(newcontent)
        """ Returns an array (newcontent is a list of contents) of a tuple and corresponding score """
        X_newcontent_counts = self._countVectorizer.transform([newcontent])
        X_newcontent_tfidf = self._tfidTransformer.transform(X_newcontent_counts)
        results = []
        for clf in self._classifierList:
            results.append(clf.predict(X_newcontent_tfidf)[0])
        counter = Counter(results)
        if (bestTag):
            #TODO if classification is diverse or evenly split, then return 'NON'
            logger.info("Prediction: \nPhrase: {0}\n Tags: {1}.".format(newcontent, str(counter)))
            mc = counter.most_common(1)[0]
            return (mc[0], mc[1]/len(self._classifierList))
        else:
            return { tag: round((c/len(self._classifierList)), 4) for tag, c in counter.items() }

#if __name__ == "__main__" : 
#    import pandas as pd
#    clfcluster = ClassifierClusterWithScoring.Unpickle(SentenceSelections.UseSentence)
#    if not clfcluster:
#        clfcluster = ClassifierClusterWithScoring()
#        rdr = SMCorpusDocumentReader(BGConfig.CorpusLocation)
#        sents = rdr.Sents()
#        data = list(map(list, zip(*sents)))
#        tags  = pd.Series(data=data[0])
#        sents = pd.Series(data=data[1])
#        clfcluster.Fit(SentenceSelections.UseSentence, sents, tags, testsize=.3)
#        # pickle classifer
#        ClassifierClusterWithScoring.Pickle(clfcluster)
#    for result in clfcluster.Predict('With MossCellTec™ No. 1, Mibelle Biochemistry offers an anti-aging treatment that is based on a novel concept:cell nucleus health.'):
#        print(result)
