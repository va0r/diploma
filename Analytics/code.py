import logging
import os
import sys
from datetime import datetime, timedelta

import pandas as pd
from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv, find_dotenv
from scipy import stats
from sqlalchemy import create_engine

from constants import columns__dict, columns__list

load_dotenv(find_dotenv())


class Analytics:
    """
    # TODO add documentation
    """

    def __init__(self, interval, days):
        self.client = Client()
        self.interval, self.days = interval, days

    @property
    def get_data(self):
        start_point = (datetime.now() - timedelta(days=self.days)).strftime("%d %B, %Y")

        try:
            df1 = pd.DataFrame(self.client.futures_historical_klines('BTCUSDT', self.interval, start_point),
                               columns=columns__list)

            df2 = pd.DataFrame(self.client.futures_historical_klines('ETHUSDT', self.interval, start_point),
                               columns=columns__list)

            try:
                # Конвертируем bigint в datetime
                df1[['Open time', 'Close time']] = df1[['Open time', 'Close time']].apply(pd.to_datetime, unit='ms')
                df2[['Open time', 'Close time']] = df2[['Open time', 'Close time']].apply(pd.to_datetime, unit='ms')

                # Подключение к базе данных PostgreSQL
                engine = create_engine(f"postgresql://{os.getenv('POSTGRES_ACCESS_LINE')}")

                # Загружаем DataFrame в базу данных
                df1.to_sql('BTCUSDT', engine, if_exists='replace', index=False, dtype=columns__dict)
                df2.to_sql('ETHUSDT', engine, if_exists='replace', index=False, dtype=columns__dict)
            except Exception as e:
                logging.exception(f'Error loading data to PostgreSQL: {e}')

            return df1.iloc[:, 4].astype(float).values, df2.iloc[:, 4].astype(float).values
        except BinanceAPIException as e:
            logging.exception(f'Analytics.get_data: {e.status_code}, {e.message}')
            sys.exit(1)

    def create_coefficients(self):
        x, y = self.get_data
        stats_lr = stats.linregress(x, y)

        return stats_lr[0], stats_lr[1]
