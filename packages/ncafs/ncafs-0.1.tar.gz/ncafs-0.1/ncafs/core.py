from typing import Tuple

import numpy as np
from scipy.optimize import minimize
from scipy.spatial.distance import pdist, squareform

from .base import BaseNCAFS


def exponential_kernel(z: np.ndarray, sigma: float) -> np.ndarray:
    """
    Exponential kernel.

    Parameters
    ----------
    z : array
        Input array
    sigma : float
        The length scale; must be a positive float.

    Returns
    -------
    array
        Transformed values.
    """
    return np.exp(-z / sigma)


def pairwise_feature_distance(X: np.ndarray, metric: str = 'cityblock') -> np.ndarray:
    """
    Calculates pairwise distances between each sample in each feature.

    Parameters
    ----------
    X : numpy.ndarray
        An (N x M) data matrix where N is the number of samples and M is the number of features.
    metric : str (optional, default='cityblock')
        Distance metric to use.

    Returns
    -------
    array
        An (M x N X N) numpy array where array[0] is the distance matrix
        representing pairwise distances between samples in feature 0.
    """
    # matrix to hold pairwise distances between samples in each feature
    N, M = X.shape
    dists = np.zeros((M, N, N))
    for j in range(M):
        dists[j] = squareform(
            pdist(
                X[:, j].reshape(-1, 1),
                metric=metric)
        )
    return dists


def add_pseudocount(v: np.ndarray) -> np.ndarray:
    """
    Adds pseudocount to avoid zero-value elements in a vector.

    Parameters
    ----------
    v : array of shape (n, 1)
        Vector that may contain undesired zeros.

    Returns
    -------
    array of shape (n, 1)
        The original vector with additive smoothing such that for every element `v_i > 0`
    """
    v = v.copy()
    mask = v == 0
    n_zeros = np.sum(mask)
    if n_zeros > 0:
        if n_zeros == len(v):
            pseudocount = np.exp(-20)
        else:
            pseudocount = np.min(v[~mask])
        v[mask] += pseudocount
    return v


def cost_nca(w: np.ndarray, feat_dist: np.ndarray, y_loss: np.ndarray,
             sigma: float = 1, alpha: float = 1) -> Tuple[float, np.ndarray]:
    """
    Cost function for NCA model.

    Parameters
    ----------
    w : array of shape (n_features,)
        weights array
    feat_dist : array of shape (n_features, n_samples, n_samples)
        Feature pairwise distance array
    y_loss : array of shape (n_samples, n_samples)
        Target values pairwise distance (loss)
    sigma : float (optional, default=1)
        The length scale of the exponential kernel; must be a positive float.
    alpha : float (optional, default=0.01)
        Regularization strength; must be a positive float.

    Returns
    -------
    cost : float
        Value of the cost function at `w`.
    gradient : array of shape (n_features,)
        Gradient vector at `w`.
    """
    M, N, _ = feat_dist.shape
    w = w.reshape((M, 1, 1))

    Dw = np.sum(feat_dist * w ** 2, axis=0)
    kDw = exponential_kernel(Dw, sigma)

    np.fill_diagonal(kDw, 0)
    row_sum = np.sum(kDw, axis=1, keepdims=True)
    row_sum = add_pseudocount(row_sum)
    p = kDw / row_sum
    # assert np.allclose(p.sum(axis=1), 1)

    E_loss = np.sum(p * y_loss, axis=1, keepdims=True)

    w = w.reshape(-1, 1)
    cost = np.mean(E_loss) + alpha * np.dot(w.T, w).item()

    s1 = np.sum(E_loss * p * feat_dist, axis=(1, 2)).reshape(-1, 1)
    s2 = np.sum(y_loss * p * feat_dist, axis=(1, 2)).reshape(-1, 1)
    grad = 2 * ((1 / sigma) * (s1 - s2) * (1 / N) + alpha) * w
    grad = grad.reshape(-1)

    return cost, grad


class NCAFSR(BaseNCAFS):
    """
    Neighborhood Component Analysis Feature Selection for regression targets.
    """

    def _fit(self, X: np.ndarray, y: np.ndarray, w0: np.ndarray) -> np.ndarray:
        n_feat = X.shape[1]
        X_dist = pairwise_feature_distance(X, metric=self.metric)
        y_dist = squareform(pdist(y.reshape(-1, 1), metric=self.metric))

        if self.alpha is None:
            alpha = self._estimate_alpha(n_feat, y_dist)
        else:
            alpha = self.alpha
        args = (X_dist, y_dist, self.sigma, alpha)
        result = minimize(cost_nca, w0, args,
                          method=self.solver,
                          jac=True,
                          options=dict(disp=False),
                          bounds=[self.bounds] * n_feat)
        return np.abs(result['x'])

    @staticmethod
    def _estimate_alpha(n_feat: int, y_dist: np.ndarray) -> float:
        # return np.log10(y_dist.mean() * n_feat) / 5
        return 0.1 * np.log10(n_feat) * np.log10(y_dist.mean())


class NCAFSC(BaseNCAFS):
    """
    Neighborhood Component Analysis Feature Selection for classification targets.
    """

    def _fit(self, X: np.ndarray, y: np.ndarray, w0: np.ndarray) -> np.ndarray:
        n_feat = X.shape[1]
        X_dist = pairwise_feature_distance(X, metric=self.metric)
        y_dist = squareform(pdist(y.reshape(-1, 1), metric=lambda u, v: 1 - (u == v)))

        if self.alpha is None:
            alpha = self._estimate_alpha(n_feat, y_dist)
        else:
            alpha = self.alpha
        args = (X_dist, y_dist, self.sigma, alpha)
        result = minimize(cost_nca, w0, args,
                          method=self.solver,
                          jac=True,
                          options=dict(disp=False),
                          bounds=[self.bounds] * n_feat)
        return np.abs(result['x'])

    @staticmethod
    def _estimate_alpha(n_feat: int, y_dist: np.ndarray) -> float:
        return 0.01 / max(1, np.log10(n_feat))
