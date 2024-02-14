import logging
import sys
from datetime import datetime, timedelta

import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv, find_dotenv
from loguru import logger
from scipy import stats

from LoguruModule.code import LoguruDecoratorClass
from PostgresDBModule.code import PostgresDBClass
from FixedVariables.constants import columns__dict, columns__list

load_dotenv(find_dotenv())


class AnalyticsClass:
    """
    # TODO add documentation
    """

    def __init__(self, interval, days):
        self.client = Client()
        self.interval, self.days = interval, days

    @property
    @LoguruDecoratorClass(level="INFO")
    def get_data(self):
        start_point = (datetime.now() - timedelta(days=self.days)).strftime("%d %B, %Y")

        try:
            create_df = lambda symbol: pd.DataFrame(
                self.client.futures_historical_klines(symbol, self.interval, start_point), columns=columns__list
            )

            df1, df2 = create_df('BTCUSDT'), create_df('ETHUSDT')

            try:
                convert_df = lambda df: df.apply(pd.to_datetime, unit='ms')
                slice__list = ['Open time', 'Close time']

                df1[slice__list], df2[slice__list] = convert_df(df1[slice__list]), convert_df(df2[slice__list])

                db = PostgresDBClass()

                db.load_dataframe(df1, 'BTCUSDT', dtype=columns__dict)
                db.load_dataframe(df2, 'ETHUSDT', dtype=columns__dict)

            except Exception as e:
                logger.add("../logfile.json", level='ERROR', format="{time} {level} {message}", serialize=True)
                logging.exception(f'Error loading data to PostgreSQL: {e}')

            return df1.iloc[:, 4].astype(float).values, df2.iloc[:, 4].astype(float).values
        except BinanceAPIException as e:
            logger.add("../logfile.json", level='ERROR', format="{time} {level} {message}", serialize=True)
            logging.exception(f'Analytics.get_data: {e.status_code}, {e.message}')
            sys.exit(1)

    @LoguruDecoratorClass(level="INFO")
    def create_coefficients(self):
        x, y = self.get_data
        stats_lr = stats.linregress(x, y)

        return stats_lr[0], stats_lr[1]
