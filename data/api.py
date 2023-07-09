from typing import List

import pandas as pd
from pandas import DataFrame
from sqlalchemy import create_engine

from context import ctx
from util.dateutil import validate_date


def get_min_bar(instrument_id: str, start_date: str, end_date: str) -> DataFrame:
    engine = create_engine(r"sqlite:///" + ctx.get_db_name())
    sql: str = f"select * from main_contract_minbar " \
               f" where instrument = '{instrument_id}' and dt between '{start_date}' and '{end_date}'"
    main_contract: DataFrame = pd.read_sql(sql, engine)
    sql: str = f"select * from non_main_contract_minbar " \
               f" where instrument = '{instrument_id}' and dt between '{start_date}' and '{end_date}'"
    non_main_contract: DataFrame = pd.read_sql(sql, engine)
    return pd.concat([main_contract, non_main_contract])


def get_main_contract(instrument: str, start_date: str, end_date: str, columns: List[str],
                      start_time: str = None, end_time: str = '23:59:00') -> DataFrame:
    instrument = instrument  # default to 'rb', may be extended to other instruments
    engine = create_engine(r"sqlite:///" + ctx.get_db_name())

    if start_time is not None:
        validate_date(start_date, '%H:%M:%S')
        validate_date(end_time, '%H:%M:%S')
        sql: str = f"select {','.join(columns)} from main_contract_minbar " \
                   f" where dt between '{start_date}' and '{end_date}' " \
                   f" and time between '{start_time}' and '{end_time}' "
    else:
        sql: str = f"select {','.join(columns)} from main_contract_minbar " \
               f" where dt between '{start_date}' and '{end_date}'"

    return pd.read_sql(sql, engine)


def get_non_main_contract(start_date: str, end_date: str, columns: List[str]) -> DataFrame:
    engine = create_engine(r"sqlite:///" + ctx.get_db_name())
    sql: str = f"select {','.join(columns)} from non_main_contract_minbar " \
               f" where dt between '{start_date}' and '{end_date}'"
    return pd.read_sql(sql, engine)


def get_table(table: str, start_date: str, end_date: str, columns: List[str]) -> DataFrame:
    engine = create_engine(r"sqlite:///" + ctx.get_db_name())
    sql: str = f"select {','.join(columns)} from {table} " \
               f" where dt between '{start_date}' and '{end_date}'"
    return pd.read_sql(sql, engine)
