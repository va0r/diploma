import logging
import os
from datetime import datetime, timedelta

import pandas as pd
from binance.client import Client
from dotenv import load_dotenv, find_dotenv

from Analytics.code import Analytics
from PostgresDB.code import PostgresDB
from TelegramMessenger.code import TelegramMessenger

load_dotenv(find_dotenv())


class Application:
    """
    # TODO add documentation
    """

    def __init__(self, interval=Client.KLINE_INTERVAL_15MINUTE, threshold=1., days=30, minutes=60):
        self.slope, self.intercept = Analytics(interval, days).create_coefficients()
        self.now, self.btcusdt, self.ethusdt, self.ethusdt_decoupled_prev = None, None, None, None
        self.threshold, self.minutes = threshold, minutes
        self.start, self.delta = datetime.utcnow(), timedelta(minutes=minutes)

    async def application(self):
        """
        # TODO add documentation
        """

        if self.ethusdt and self.btcusdt:
            ethusdt_decoupled = abs(self.ethusdt - (self.intercept + self.slope * self.btcusdt))

            if (self.now - self.start) < self.delta:
                if not self.ethusdt_decoupled_prev:
                    self.ethusdt_decoupled_prev = ethusdt_decoupled
                percentage = abs((ethusdt_decoupled - self.ethusdt_decoupled_prev) / self.ethusdt_decoupled_prev * 100)
                self.ethusdt_decoupled_prev = ethusdt_decoupled
                if percentage >= self.threshold:
                    message = (f'{percentage:.4f}% change of the BTCUSDT free ETHUSDT price {ethusdt_decoupled:.4f} '
                               f'within {self.minutes} minutes '
                               f'starting from {self.start.strftime("%Y-%m-%d %H:%M:%S")} UTC')
                    try:
                        await TelegramMessenger(os.getenv('BOT_TOKEN')).send_message(os.getenv('TELEGRAM_ID'), message)
                    except Exception as e:
                        logging.exception(f'Process.application: {e.__dict__}')
                    print(message)

                    data__dict = {
                        'datetime': self.now,
                        'ethusdt': self.ethusdt,
                        'btcusdt': self.btcusdt,
                        'ethusdt_decoupled': ethusdt_decoupled,
                        'percentage': percentage,
                    }

                    df = pd.DataFrame([data__dict])

                    db = PostgresDB()
                    db.load_dataframe(df, 'SESSION', if_exists='append')

            else:
                self.start = self.now
                self.ethusdt_decoupled_prev = None
