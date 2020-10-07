# import pandas as pd
# import numpy as np
# import cvxpy as cp
from pypfopt import risk_models
# from pypfopt import expected_returns
# from pypfopt import EfficientFrontier
# from pypfopt import objective_functions
# from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices
# from pypfopt import HRPOpt
# from pypfopt import CLA
# from pypfopt import black_litterman
# from pypfopt import BlackLittermanModel
# from pypfopt import plotting


import pandas_datareader.data as web
from datetime import datetime
import matplotlib.pylab as plt
import pandas as pd
dfs = {}
for ticker in ['AAPL', 'MSFT', 'KO']:
    df = web.DataReader(ticker, 'stooq', '2020-01-01', '2020-09-30', api_key='6JUN1FV7A3MTWJ1Y')
    dfs[ticker] = df["Close"]
stock_data = pd.DataFrame(dfs)
stock_data.sort_index(inplace=True)
risk_models.sample_cov(stock_data)
print(stock_data)
