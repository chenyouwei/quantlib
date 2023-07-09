from pathlib import Path
import pandas as pd
from context import ctx
from sqlalchemy import create_engine
from util import logger


def persist_min_bar_from_csv():
    engine = create_engine(r"sqlite:///" + ctx.get_db_name())

    logger.info("Persisting Main Contract Data...")
    file_path: str = str(Path(__file__).parent.parent.parent) + r'/resource/data/main_contract_hist.csv'
    main_contract_hist: pd.DataFrame = pd.read_csv(file_path)
    main_contract_hist.to_sql(f"main_contract_minbar", engine, if_exists='replace', index=False, method='multi', chunksize=10000)

    logger.info("Persisting Non-main Contract Data...")
    file_path: str = str(Path(__file__).parent.parent.parent) + r'/resource/data/non_main_contract_hist.csv'
    non_main_contract_hist: pd.DataFrame = pd.read_csv(file_path)
    non_main_contract_hist.to_sql(f"non_main_contract_minbar", engine, if_exists='replace', index=False, method='multi', chunksize=10000)
