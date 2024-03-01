from typing import Tuple, List, Optional
import numpy as np

import logging

logger = logging.getLogger(__name__)


def linear_regression(
    features: np.ndarray,
    outcomes: np.ndarray,
) -> Tuple[np.ndarray, float]:
    """Perform linear regression.

    Finding linear coefficients A and bias b that minimize the mean squared error ||Y - AX - b||^2, where X is features, Y is outcomes.

    Args:
        features: 2D array of shape (n_samples, n_features), i.e. X.
        outcomes: 2D array of shape (n_samples, n_outcomes), i.e. Y.

    Returns:
        linear_coeffs: 1D array of length n_features, i.e. A.
        bias: Bias, i.e. b.

    Raises:
        ValueError: An error occurred when the counts of features and outcomes are not the same.
        numpy.linalg.LinAlgError: An error occurred when SVD does not converge.
    """
    logger.info("Running linear regression")
    logger.debug("features:\n{}".format(features))
    logger.debug("outcomes:\n{}".format(outcomes))

    if not len(features) == len(outcomes):
        logger.error(
            "Not equal lengths:\n{} features\n{} outcomes".format(
                len(features), len(outcomes)
            )
        )
        raise ValueError("The counts of features and outcomes are not the same!")
    num = len(features)
    X = np.array(features, dtype=float).reshape(num, -1)
    y = np.array(outcomes, dtype=float)

    ones = np.ones((X.shape[0], 1))
    X1 = np.hstack((X, ones))

    try:
        A = np.linalg.pinv(X1.T @ X1) @ X1.T @ y
    except np.linalg.LinAlgError as e:
        logger.error("SVD does not converge when updating linear coefficients!")
        raise e

    linear_coeffs, bias = A[:-1], A[-1]
    logger.info("Linear regression completed")
    logger.debug("Linear coefficients: {}".format(linear_coeffs))
    logger.debug("Bias: {}".format(bias))
    return linear_coeffs, bias


def causal_regression(
    confounders: np.ndarray,
    outcomes: np.ndarray,
    treatments: Optional[np.ndarray] = None,
    sigma: float = 2.0,
    tol=1e-2,
    max_num_iter=10000,
) -> Tuple[np.ndarray, float]:
    """Perform causal regression."""
    logger.info("Running causal regression")
    logger.debug("outcomes:\n{}".format(outcomes))
    logger.debug("confounders:\n{}".format(confounders))
    logger.debug("treatments:\n{}".format(treatments))

    if treatments is None:
        treatments = np.empty((len(outcomes), 0))
        logger.info("treatments:\n{}".format(treatments))
        logger.info("len(treatments):\n{}".format(len(treatments)))

    if not len(treatments) == len(outcomes) == len(confounders):
        logger.error(
            "Not equal lengths:\n{} treatments\n{} outcomes\n{} confounders".format(
                len(treatments), len(outcomes), len(confounders)
            )
        )
        raise ValueError(
            "The counts of treatments, outcomes and confounders are not the same!"
        )
    num = len(treatments)

    X = np.array(treatments, dtype=float).reshape(num, -1)

    ones = np.ones((len(X), 1), dtype=float)
    X1 = np.hstack((X, ones))
    dim_X1 = X1.shape[1]

    try:
        y = np.array(outcomes, dtype=float)
        assert y.ndim == 1
    except Exception:
        logger.error(
            "Require 1-dimensional outcome, but got:\n{} dim outcome\n".format(y.ndim)
        )
        raise ValueError("Causal regression only supports 1-dimensional outcome!")

    Z = np.array(confounders, dtype=float).reshape(num, -1)
    dim_Z = Z.shape[1]

    logger.debug("Initializing matrix A with linear coefficient")

    linear_coefs, bias = linear_regression(np.hstack((X, Z)), y)
    a = np.insert(linear_coefs, dim_X1 - 1, bias)

    """
    sigma = (SE / 2) ** 0.5
    """

    logger.debug("Approaching causal entropy through an iterative method")
    causal_entropy_estimates: List[float] = []
    for k in range(max_num_iter):
        aX1 = np.einsum("i,ji", a[:dim_X1], X1)
        aZ = np.einsum("i,ji", a[dim_X1:], Z)
        square_error = ((y - aX1)[:, np.newaxis] - aZ[np.newaxis, :]) ** 2

        P = 1 / (sigma * np.sqrt(2 * np.pi)) * np.exp(-square_error / (2 * sigma**2))

        mean_P = P.mean(1, keepdims=True)
        causal_entropy_estimates.append(-np.log(mean_P).mean())
        W = P / mean_P

        EWX1ZtX1Z = np.zeros((dim_X1 + dim_Z, dim_X1 + dim_Z), dtype=float)

        W0 = W.sum(axis=1)
        EWX1ZtX1Z[:dim_X1, :dim_X1] = np.einsum("j,jk,jl", W0, X1, X1)

        WX1Z = np.einsum("ij,ik,jl", W, X1, Z)
        EWX1ZtX1Z[:dim_X1, dim_X1:] = WX1Z
        EWX1ZtX1Z[dim_X1:, :dim_X1] = WX1Z.T

        W1 = W.sum(axis=0)
        EWX1ZtX1Z[dim_X1:, dim_X1:] = np.einsum("j,jk,jl", W1, Z, Z)

        EWX1ZtX1Z /= len(X1) ** 2

        EWX1Zty = np.zeros(dim_X1 + dim_Z, dtype=float)
        EWX1Zty[:dim_X1] = np.einsum("j,jk,j", W0, X1, y)
        EWX1Zty[dim_X1:] = np.einsum("ij,jk,i", W, Z, y)
        EWX1Zty /= len(X1) ** 2

        logger.debug("Checking convergence")
        if k == max_num_iter - 1 or (
            len(causal_entropy_estimates) > 1
            and abs(causal_entropy_estimates[-1] - causal_entropy_estimates[-2]) < tol
        ):
            coefficients = a
            causal_entropy = causal_entropy_estimates[-1]

            logger.info("Causal regression completed")
            logger.debug(">>>>>> coefficients:\n{}".format(coefficients))
            logger.debug(">>>>>> causal_entropy:\n{}".format(causal_entropy))
            return coefficients, causal_entropy

        logger.debug("Updating coefficient matrix A")
        try:
            a = np.linalg.pinv(EWX1ZtX1Z) @ EWX1Zty
        except np.linalg.LinAlgError as e:
            logger.error("SVD does not converge when updating coefficient matrix A!")
            raise e

    logger.error(
        "Causal regression does not converge within {} iterations".format(max_num_iter)
    )
    raise RuntimeError("Causal regression does not converge!")
