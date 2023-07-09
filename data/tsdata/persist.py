import tushare as ts
from datetime import datetime, timedelta
import pandas as pd
from context import ctx
from sqlalchemy import create_engine
from util import logger

exchange_markerts = ['SSE', 'SZSE', 'CFFEX', 'SHFE', 'CZCE', 'DCE', 'INE']
exchange_markerts_dict = {
    'SSE': '上交所',
    'SZSE': '深交所,',
    'CFFEX': '中金所',
    'SHFE': '上期所',
    'CZCE': '郑商所',
    'DCE': '大商所',
    'INE': '上能源',
}

_ts_secret_key = '3204fc11390d6b3357326e0d8f482728fba18cef49dacc1f0f8bf2c9'


def persist_exchange_calender(exchange: str = 'SHFE', start_date: str = '20180101',
                              end_date: str = datetime.strftime(datetime.now() + timedelta(days=180),
                                                                '%Y%m%d')) -> None:
    pro = ts.pro_api(_ts_secret_key)
    df: pd.DataFrame = pro.trade_cal(exchange=exchange, start_date=start_date, end_date=end_date)
    engine = create_engine(r"sqlite:///" + ctx.get_db_name())
    df.to_sql(f"{exchange}_EXCHANGE_CALENDER", engine, if_exists='replace', index=False, method='multi')


def persist_all_exchange_calender() -> None:
    for market in exchange_markerts:
        logger.info(f"Persisting {exchange_markerts_dict[market]} Calender...")
        persist_exchange_calender(market)
