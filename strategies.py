from dataclasses import dataclass
from typing import Dict

from pypfopt import objective_functions
from pypfopt import EfficientFrontier
from pypfopt import risk_models
import numpy as np
import pandas as pd


@dataclass
class MinVarianceAuxiliaryData:
    covariance: pd.DataFrame


def min_variance_portfolio(timestamp, returns_excluding_today) -> Dict[str, float]:
    # print("Optimizing portfolio for", timestamp)
    # print("returns_excluding_today", returns_excluding_today)
    # S = risk_models.semicovariance(returns_excluding_today, returns_data=True)
    S = risk_models.CovarianceShrinkage(returns_excluding_today, returns_data=True).ledoit_wolf()
    ef = EfficientFrontier(np.zeros(returns_excluding_today.columns.size), S)
    # ef.add_objective(objective_functions.L2_reg, gamma=.05)
    ef.min_volatility()
    weights = ef.clean_weights()
    return weights, MinVarianceAuxiliaryData(covariance=S)
