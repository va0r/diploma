import logging
import os
from datetime import datetime, timedelta

import pandas as pd
from binance.client import Client
from dotenv import load_dotenv, find_dotenv
from loguru import logger

from AnalyticsModule.code import AnalyticsClass
from ApplicationModule.pcb import print_colored_and_boxed
from PostgresDBModule.code import PostgresDBClass
from TelegramMessengerModule.code import TelegramMessengerClass

load_dotenv(find_dotenv())


class ApplicationClass:
    """
    Класс для работы с текущими данными криптовалют.

    Получает текущие данные из Binance с помощью пакета python-binance.

    Считает очищенные данные для тикета ETHUSDT, при соблюдении условий срабатывания триггеров --
    печатает данные в консоль и посылает сообщение через тг-бот.

    Args:
        interval (int): отсечки времени получения цены криптовалюты (измеряется в минутах/часах/днях)
        threshold (float): триггер срабатывания оповещения об изменении цены ETHUSDT (по умолчанию 1%)
        days (int): период времени, за который получаются исторические данные (измеряется в днях)
        minutes (int): период времени, на котором слушается цена криптовалют (изменяется в минутах, по умолчанию 60 минут)

    Raises:
        Exception: если не удается отправить сообщение через тг-бот.
    """

    def __init__(self, interval=Client.KLINE_INTERVAL_15MINUTE, threshold=1., days=30, minutes=60):
        self.slope, self.intercept = AnalyticsClass(interval, days).create_coefficients()
        self.now, self.btcusdt, self.ethusdt, self.ethusdt_decoupled_prev = None, None, None, None
        self.threshold, self.minutes = threshold, minutes
        self.start, self.delta = datetime.utcnow(), timedelta(minutes=minutes)

    @logger.catch()
    async def application(self):
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
                        await TelegramMessengerClass(os.getenv('BOT_TOKEN')).send_message(os.getenv('TELEGRAM_ID'),
                                                                                          message)
                    except Exception as e:
                        logfile_path = os.path.join(os.getcwd(), "logfile.json")
                        logger.add(logfile_path, level='ERROR', format="{time} {level} {message}", serialize=True)
                        logging.exception(f'Process.application: {e.__dict__}')
                    print_colored_and_boxed(message)

                    data__dict = {
                        'datetime': self.now,
                        'ethusdt': self.ethusdt,
                        'btcusdt': self.btcusdt,
                        'ethusdt_decoupled': ethusdt_decoupled,
                        'percentage': percentage,
                    }

                    df = pd.DataFrame([data__dict])

                    db = PostgresDBClass()
                    db.load_dataframe(df, 'SESSION')

            else:
                self.start = self.now
                self.ethusdt_decoupled_prev = None
