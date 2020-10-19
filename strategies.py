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
    print("Optimizing portfolio for", timestamp)
    S = risk_models.CovarianceShrinkage(returns_excluding_today, returns_data=True).ledoit_wolf()
    # S = risk_models.exp_cov(returns_excluding_today, returns_data=True)
    ef = EfficientFrontier(np.zeros(returns_excluding_today.columns.size), S)
    ef.add_objective(objective_functions.L2_reg, gamma=.05)
    ef.min_volatility()
    weights = ef.clean_weights()
    return weights, MinVarianceAuxiliaryData(covariance=S)
