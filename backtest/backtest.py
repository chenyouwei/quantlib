import numpy as np

from .metric import *


def backtest(net_worth_array: np.ndarray[float]) -> None:

    ret = total_returns(net_worth_array)
    annualized_ret = total_annualized_returns(net_worth_array)
    sharpe_ratio = sharpe(net_worth_array)
