# https://scikit-learn.org/stable/developers/develop.html
# https://github.com/scikit-learn-contrib/project-template/blob/master/skltemplate/_template.py

from abc import ABC, abstractmethod
from typing import Optional, Tuple

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import KFold
from sklearn.preprocessing import StandardScaler
from sklearn.utils.validation import (
    check_X_y,
    check_array,
    check_is_fitted,
    check_scalar
)


class BaseNCAFS(TransformerMixin, BaseEstimator, ABC):
    """

    Parameters
    ----------
    n_features_to_select : int (optional, default=None)
        Number of features which must be selected.
    threshold : float (optional, default=0.1)
        Used only when `n_features_to_select=None`. Select features whose weight is greater then `threshold`.
    alpha : float (optional, default=None)
        Regularization strength; must be a positive float. If None, then it is automatically set based on an heuristic.
    sigma : float (optional, default=1)
        The length scale of the exponential kernel; must be a positive float.
    metric : str (optional, default='cityblock')
        The metric used to calculate pairwise feature distances.
    standardize : bool (optional, default=True)
        Whether to standardize feature values.
    fit_method : str (optional, default='full')
        If 'full', solves the optimization problem using the whole dataset at once. If 'average', splits the data into
        folds and returns the average of the feature weights by fold.
    n_splits : int (optional, default=3)
        Number of folds to split the data into when `fit_method='average'`.
    solver : str (optional, default='L-BFGS-B')
        The solver method used for minimization of the NCA cost function.
    """

    def __init__(
            self,
            n_features_to_select: Optional[int] = None,
            threshold: float = 1e-1,
            alpha: float = None,
            sigma: float = 1.0,
            metric: str = 'cityblock',
            standardize: bool = True,
            fit_method: str = 'full',
            n_splits: int = 3,
            solver='L-BFGS-B',
            bounds: Tuple[float, float] = (0, 10),
    ):
        check_scalar(threshold, 'threshold', (float, int), min_val=0)
        check_scalar(sigma, 'sigma', (float, int), min_val=1e-7)
        check_scalar(n_splits, 'n_split', int, min_val=2)

        if alpha is not None:
            check_scalar(alpha, 'alpha', (float, int), min_val=0)

        self.n_features_to_select = n_features_to_select
        self.threshold = threshold
        self.alpha = alpha
        self.sigma = sigma
        self.metric = metric
        self.standardize = standardize
        self.fit_method = fit_method
        self.n_splits = n_splits
        self.solver = solver
        self.bounds = bounds

    @abstractmethod
    def _fit(self, X: np.ndarray, y: np.ndarray, w0: np.ndarray) -> np.ndarray:
        pass

    @staticmethod
    @abstractmethod
    def _estimate_alpha(n_feat: int, y_dist: np.ndarray) -> float:
        pass

    def fit(self, X, y, w0=None):
        """
        Fit the NCAFS model.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.
        w0 : array of shape (n_features,)
            The initial weight values.
        """
        X_, y_ = check_X_y(X, y, accept_sparse=False, y_numeric=True)
        y_ = y_.reshape(-1, 1)
        n_inst, n_feat = X_.shape

        if self.standardize:
            scaler = StandardScaler()
            X_ = scaler.fit_transform(X_)

        if w0 is None:
            w0 = np.ones(n_feat)

        if self.fit_method == 'full':
            w = self._fit(X_, y_, w0)
        elif self.fit_method == 'average':
            w_fold = []
            kf = KFold(n_splits=self.n_splits, shuffle=False)
            for _, index in kf.split(X_):
                w_fold.append(self._fit(X_[index], y_[index], w0))
            w_fold = np.array(w_fold)
            w = w_fold.mean(axis=0)
        else:
            if isinstance(self.fit_method, str):
                raise ValueError(f"Unknown fit method '{self.fit_method}'. It must be either 'full' or 'average'.")
            else:
                raise TypeError("Parameter 'fit_method' must be of string type.")

        n_feat_select = self.n_features_to_select
        if n_feat_select is None:
            self.support_ = (w > self.threshold)
            self.n_features_ = np.sum(self.support_)
        elif isinstance(n_feat_select, int):
            if 0 < n_feat_select < n_feat:
                first_n_feat_ind = np.argsort(w)[::-1][:n_feat_select]
                support = np.zeros(w.shape, dtype=bool)
                support[first_n_feat_ind] = True
                self.support_ = support
                assert np.sum(support) == n_feat_select
                self.n_features_ = n_feat_select
            else:
                raise ValueError("n_features_to_select must be greater than zero and less than the number of features.")
        else:
            raise TypeError("n_features_to_select must be either None or integer.")

        self.weights_ = w
        self.X_ = X_
        self.y_ = y_

        return self

    def transform(self, X) -> np.ndarray:
        """
        Reduce X to the selected features.

        Parameters
        ----------
        X : array of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        X_r : array of shape (n_samples, n_selected_features)
            The input samples with only the selected features.
        """
        check_is_fitted(self, ['weights_', 'support_', 'n_features_'])
        X_ = check_array(X)
        return X_[:, self.support_]
