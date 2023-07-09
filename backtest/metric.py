import numpy as np
from context import ctx


# Attention: all metrics are calculated based on daily net worth
# TODO
# ret, annual_ret, win_ratio
# sharpe, sotio

def total_returns(net_worth_array: np.ndarray[float]) -> float:
    assert(net_worth_array[0] == 1.0)
    return net_worth_array[-1] - 1.0


def total_annualized_returns(net_worth_array: np.ndarray[float]) -> float:
    num_of_days = net_worth_array.size[0] - 1
    return (1 + total_returns(net_worth_array)) ** (250 / num_of_days)


def sharpe(net_worth_array: np.ndarray[float]) -> float:
    sigma = np.std(ddof=1)
    return (total_annualized_returns(net_worth_array) - ctx.get_risk_free_ratio()) / sigma
