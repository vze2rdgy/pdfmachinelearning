from abc import ABC, abstractmethod

class SMEstimatorBase(object):
    """A generic class for all classifiers used in this library."""

    @abstractmethod
    def Fit(self, *, train_test_split_value = 0.0, usePipeLine=True):
        raise NotImplementedError()

    @abstractmethod
    def Predict(self, newcontent):
        raise NotImplementedError()



