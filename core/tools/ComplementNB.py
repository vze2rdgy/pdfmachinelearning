from sklearn.naive_bayes import BaseDiscreteNB
import numpy as np
from scipy.sparse import issparse
from sklearn.utils.extmath import safe_sparse_dot
from sklearn.utils.validation import check_is_fitted
from sklearn.utils import check_X_y, check_array, check_consistent_length

class ComplementNB(BaseDiscreteNB):
    """The Complement Naive Bayes classifier described in Rennie et al. (2003).
    The Complement Naive Bayes classifier was designed to correct the "severe
    assumptions" made by the standard Multinomial Naive Bayes classifier. It is
    particularly suited for imbalanced data sets.
    Read more in the :ref:`User Guide <complement_naive_bayes>`.
    Parameters
    ----------
    alpha : float, optional (default=1.0)
        Additive (Laplace/Lidstone) smoothing parameter (0 for no smoothing).
    fit_prior : boolean, optional (default=True)
        Only used in edge case with a single class in the training set.
    class_prior : array-like, size (n_classes,), optional (default=None)
        Prior probabilities of the classes. Not used.
    norm : boolean, optional (default=False)
        Whether or not a second normalization of the weights is performed. The
        default behavior mirrors the implementations found in Mahout and Weka,
        which do not follow the full algorithm described in Table 9 of the
        paper.
    Attributes
    ----------
    class_log_prior_ : array, shape (n_classes, )
        Smoothed empirical log probability for each class. Only used in edge
        case with a single class in the training set.
    feature_log_prob_ : array, shape (n_classes, n_features)
        Empirical weights for class complements.
    class_count_ : array, shape (n_classes,)
        Number of samples encountered for each class during fitting. This
        value is weighted by the sample weight when provided.
    feature_count_ : array, shape (n_classes, n_features)
        Number of samples encountered for each (class, feature) during fitting.
        This value is weighted by the sample weight when provided.
    feature_all_ : array, shape (n_features,)
        Number of samples encountered for each feature during fitting. This
        value is weighted by the sample weight when provided.
    Examples
    --------
    >>> import numpy as np
    >>> X = np.random.randint(5, size=(6, 100))
    >>> y = np.array([1, 2, 3, 4, 5, 6])
    >>> from sklearn.naive_bayes import ComplementNB
    >>> clf = ComplementNB()
    >>> clf.fit(X, y)
    ComplementNB(alpha=1.0, class_prior=None, fit_prior=True, norm=False)
    >>> print(clf.predict(X[2:3]))
    [3]
    References
    ----------
    Rennie, J. D., Shih, L., Teevan, J., & Karger, D. R. (2003).
    Tackling the poor assumptions of naive bayes text classifiers. In ICML
    (Vol. 3, pp. 616-623).
    https://people.csail.mit.edu/jrennie/papers/icml03-nb.pdf
    """

    def __init__(self, alpha=1.0, fit_prior=True, class_prior=None,
                 norm=False):
        self.alpha = alpha
        self.fit_prior = fit_prior
        self.class_prior = class_prior
        self.norm = norm

    def _count(self, X, Y):
        """Count feature occurrences."""
        if np.any((X.data if issparse(X) else X) < 0):
            raise ValueError("Input X must be non-negative")
        self.feature_count_ += safe_sparse_dot(Y.T, X)
        self.class_count_ += Y.sum(axis=0)
        self.feature_all_ = self.feature_count_.sum(axis=0)

    def _update_feature_log_prob(self, alpha):
        """Apply smoothing to raw counts and compute the weights."""
        comp_count = self.feature_all_ + alpha - self.feature_count_
        logged = np.log(comp_count / comp_count.sum(axis=1, keepdims=True))
        # BaseNB.predict uses argmax, but ComplementNB operates with argmin.
        feature_log_prob = -logged
        if self.norm:
            summed = logged.sum(axis=1, keepdims=True)
            feature_log_prob = -feature_log_prob / summed
        self.feature_log_prob_ = feature_log_prob

    def _joint_log_likelihood(self, X):
        """Calculate the class scores for the samples in X."""
        check_is_fitted(self, "classes_")

        X = check_array(X, accept_sparse="csr")
        jll = safe_sparse_dot(X, self.feature_log_prob_.T)
        if len(self.classes_) == 1:
            jll += self.class_log_prior_
        return jll
