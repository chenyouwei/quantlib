from typing import List

from backtest.account import FutureAccount
from pathlib import Path
from collections import namedtuple


class Context:

    _start_date: str
    _freq: str
    _frequency_set: str = {'DAILY', 'MINUTE'}
    _risk_free_ratio: float = 0.04
    _price_slippage: float = 1.1

    _current_timestamp: str  # format: "yyyy-mm-dd HH:MM:SS"
    _account: FutureAccount
    _db_name: str = str(Path(__file__).parent.parent) + r'/resource/quantlib.db'

    def __init__(self) -> None:
        self._account = FutureAccount(balance=100000)

    def get_risk_free_ratio(self) -> float:
        return self._risk_free_ratio

    def get_current_timestamp(self) -> str:
        return self._current_timestamp

    def set_current_timestamp(self, timestamp: str) -> None:
        self._current_timestamp = timestamp

    def set_frequency(self, freq: str) -> None:
        if freq not in self._frequency_set:
            raise ValueError(f"frequency must be in {self._frequency_set}, Your frequency: {freq}")
        self._freq = freq

    def get_db_name(self) -> str:
        return self._db_name

    def get_account(self) -> FutureAccount:
        return self._account

    def get_price_slippage(self) -> float:
        return self._price_slippage

    def __str__(self):
        pass


def run_daily() -> None:
    pass


def scheduler(period: int = 1, skip_last: int = 0) -> None:
    """ This scheduler is only for backtesting
    :return:
    """
    _market_open_time: List[str] = ["09:00", "10:30", "13:30", "21:00"]
    _market_close_time: List[str] = ["10:15", "11:30", "15:00", "23:30"]

    # spawn run time point
    for open_time, close_time in zip(_market_open_time, _market_close_time):
        pass


def run_minute(period: int = 1, skip_last: int = 0) -> None:
    # update ctx current timestamp
    pass


# global contex
ctx = Context()
