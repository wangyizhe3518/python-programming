import pytest
import numpy as np
import pandas as pd
import logging

from context import linear_regression, causal_regression

logger = logging.getLogger(__name__)


@pytest.mark.parametrize(
    "features, outcomes",
    [
        (np.array([[1, 0], [0, 1]]), np.array([5, 6])),
        (np.array([[1, 2], [3, 4]]), np.array([5, 6])),
    ],
)
def test_linear_regression(features, outcomes, caplog):
    caplog.set_level(logging.INFO)
    linear_coeffs, bias = linear_regression(features, outcomes)
    logger.debug("linear_coeffs:\n{}".format(linear_coeffs))
    logger.debug("bias:\n{}".format(bias))


@pytest.mark.parametrize(
    "confounders, outcomes, treatments",
    [
        (
            pd.DataFrame(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                ]
            ),
            pd.Series([2, 7, 8]),
            pd.Series([1, 3, 7]),
        ),
        (
            pd.DataFrame(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                ]
            ),
            pd.Series([2, 7, 8]),
            pd.DataFrame([1, 3, 7]),
        ),
        (
            pd.DataFrame(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                ]
            ),
            pd.Series([2, 7, 8]),
            pd.DataFrame(
                [
                    [1, 5],
                    [3, 4],
                    [7, 1],
                ]
            ),
        ),
        (
            pd.DataFrame(
                [
                    [1, 2, 3],
                    [4, 5, 6],
                    [7, 8, 9],
                    [9, 8, 9],
                ]
            ),
            pd.Series([2, 7, 8, 9]),
            None,
        ),
    ],
)
def test_causal_regression(confounders, outcomes, treatments, caplog):
    caplog.set_level(logging.INFO)
    coeffs, causal_entropy = causal_regression(confounders, outcomes, treatments)
    logger.debug("coeffs:\n{}".format(coeffs))
    logger.debug("causal_entropy:\n{}".format(causal_entropy))
