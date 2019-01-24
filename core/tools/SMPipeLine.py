from . import SMEstimatorBase

class SMPipeLine(SMEstimatorBase.SMEstimatorBase):
    """
    #TODO: The current classifiers need changes to accept
            piped data to fit and predict.
    A pipeline keeps a collection of word estimators. 
    By passing from the top to the bottom of the list of
    estimators, the accuracy of auto tagging of any 
    phrase of sentence is increased.
    """

    __slots__ = [
        _elist # list of estimators.
        ]

    def __init__(self, *args):
        self._elist = *args

    def Fit(self, *, train_test_split_value = 0.0, usePipeLine=True):
        return

    def Predict(self, newcontent):
        return


