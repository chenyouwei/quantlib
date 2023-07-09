from typing import List, Dict, Tuple

import numpy as np
from collections import namedtuple


class Account:

    balance: float
    stock_asset: float
    frequency: str
    start_date: str

    _record_exchange_timestamp: List[str]  # timestamp format yyyy-mm-dd HH:MM:SS
    _record_exchange: List[str]
    _record_net_worth: List[float]
    _directions = {'LONG', 'SHORT'}
    _net_value_array: np.ndarray
    _hold_stocks: Dict[str, Tuple[float, int]]

    def __init__(self, balance: int) -> None:
        self.balance = balance

    def get_balance(self) -> float:
        """
        Args:
            balance: balance of account

        :return:
        """
        return self.balance


class FutureAccount:

    balance: float
    stock_asset: float
    frequency: str
    start_date: str

    TRADE_HIST_NAMED_TUPLE = namedtuple('TRADE_HIST_NAMED_TUPLE', 'timestamp, instrument, price, amount, direction',
                                        defaults=(None, ) * 5)
    POSITION_NAMED_TUPLE = namedtuple('POSITION_NAMED_TUPLE', 'amount, trade_price', defaults=(None, ) * 2)

    _record: List[TRADE_HIST_NAMED_TUPLE]
    _record_trade: List[Tuple[str, str, str, int, str]]  # timestamp, instrument, price, amount, direction
    _record_daily_balance: List[float]
    _net_value_array: np.ndarray[float]
    _position: Dict[POSITION_NAMED_TUPLE]

    user_data = {}

    def __init__(self, balance: int) -> None:
        self.balance = balance

    def get_balance(self) -> float:
        return self.balance

    def set_balance(self, cost) -> None:
        self.balance += cost

    @property
    def position(self):
        return self._position

    @property
    def record_trade(self):
        return self._record_trade




