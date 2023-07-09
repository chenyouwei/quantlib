"""
模拟交易
"""
from enum import Enum
from typing import Tuple, Optional

from pandas import DataFrame

from backtest.account import FutureAccount
from util.dateutil import validate_date
from data.api import get_table, get_main_contract
from context import ctx

_trade_direction = {'long', 'short'}
_tigger_direction = {'greater', 'smaller'}  # all contain '='
_instrument_mapping = {'rb': '', }


def _transaction_price(instrument: str, date: str, trigger_price: float, exchange_price: float,
                       tigger_dir: str = 'smaller', direction: str = 'long') -> Optional[Tuple[str, float]]:
    """
    :param instrument: 标的
    :param date: 下单时间 format: yyyy-mm-dd HH:MM
    :param trigger_price: 触发价格
    :return: 交易时间，成交价格
    """
    validate_date(date, '%Y-%m-%d %H:%M:%S')
    if direction not in _trade_direction:
        raise ValueError(f"direction must be in {_trade_direction}, your direction: {direction}")

    dt, time = date.split(' ')
    market_data = get_main_contract(instrument, date, date, ['instrument', 'time', 'high', 'low'], time)
    market_data.sort_values(by='time', ascending=True, inplace=True)

    if direction == 'long':
        if tigger_dir == 'smaller':
            assert exchange_price >= trigger_price
            trigger_point: DataFrame = market_data[market_data['high'] <= trigger_price]

            if trigger_point.empty:
                return None

            bar_low, bar_high = trigger_point['low'].iloc[0], trigger_point['high'].iloc[0]

            # 成交逻辑
            if bar_low <= exchange_price <= bar_high:
                return trigger_point['time'].iloc[0], exchange_price * ctx.get_price_slippage()
            elif exchange_price > bar_high:
                return trigger_point['time'].iloc[0], bar_high * ctx.get_price_slippage()

            return trigger_point['time'].iloc[0], trigger_point['high'].iloc[0]
        else:
            raise NotImplementedError('Not Implement Yet.')
    else:
        trigger_point: DataFrame = market_data[market_data['high'] <= trigger_price]

        if trigger_point.empty:
            return None

        bar_low, bar_high = trigger_point['low'].iloc[0], trigger_point['high'].iloc[0]

        # 成交逻辑
        if bar_low <= exchange_price <= bar_high:
            return trigger_point['time'].iloc[0], exchange_price
        elif exchange_price < bar_low:
            return trigger_point['time'].iloc[0], bar_low

        return trigger_point['time'].iloc[0], trigger_point['high'].iloc[0]


def order_target(instrument: str, date: str, trigger_price: float, exchange_price: float,
                 amount: int, direction) -> Tuple[bool, str]:
    """
    :param instrument: 标的
    :param date: 下单时间 format: yyyy-mm-dd HH:MM:SS
    :param trigger_price: 触发价格
    :param exchange_price: 交易价格
    :param amount: 交易量（手数）
    :param direction: 交易方向（开平仓）
    :return:
    """

    if direction not in _trade_direction:
        raise ValueError(f"direction must be in {_trade_direction}, your direction: {direction}")

    if direction == 'long':
        trans = _transaction_price(instrument, date, trigger_price, exchange_price)
        if trans is None:
            return False, "tigger price failed."

        trade_time, trade_price = trans
        trade_cost = trade_price * amount
        if trade_cost > ctx.get_account().get_balance():
            return False, "short of balance"

        # update balance
        ctx.get_account().set_balance(-trade_cost)
        # update trade history
        ctx.get_account().record_trade.append(FutureAccount.TRADE_HIST_NAMED_TUPLE(timestamp=date + ' ' + trade_time,
                                                                                   instrument=instrument,
                                                                                   price=trade_price,
                                                                                   amount=amount,
                                                                                   direction=direction))
        # update position
        if instrument not in ctx.get_account().position:
            ctx.get_account().position[instrument] = FutureAccount.POSITION_NAMED_TUPLE(trade_price=trade_price,
                                                                                        amount=amount)
        else:
            prev_position: FutureAccount.POSITION_NAMED_TUPLE = ctx.get_account().position[instrument]
            prev_price, prev_amount = prev_position.trade_price, prev_position.amount
            cur_amount = amount + prev_amount
            cur_price = (prev_price * prev_amount + trade_cost) / cur_amount

            ctx.get_account().position[instrument] = FutureAccount.POSITION_NAMED_TUPLE(trade_price=cur_price,
                                                                                        amount=cur_amount)
    else:
        # 平仓
        1 == 1
