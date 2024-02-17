import asyncio
import logging
import os
import sys
from datetime import datetime

from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv, find_dotenv
from loguru import logger

from ApplicationModule.code import ApplicationClass
from ApplicationModule.pcb import print_colored_and_boxed
from LoguruModule.code import LoguruDecoratorClass

load_dotenv(find_dotenv())


class Process(ApplicationClass):
    """
    # TODO add documentation
    """

    @LoguruDecoratorClass(level="INFO")
    async def futures_listener(self, client):
        """
        # TODO add documentation
        """

        try:
            async with BinanceSocketManager(client).all_ticker_futures_socket() as stream:
                while True:
                    res = await stream.recv()
                    if res['data']['s'] == 'BTCUSDT':
                        self.btcusdt = float(res['data']['a'])
                    if res['data']['s'] == 'ETHUSDT':
                        self.ethusdt = float(res['data']['a'])
                        self.now = datetime.utcfromtimestamp(res['data']['E'] / 1000)
                    loop.call_soon(asyncio.create_task, self.application())
        except BinanceAPIException as e:
            logfile_path = os.path.join(os.getcwd(), "logfile.json")
            logger.add(logfile_path, level='ERROR', format="{time} {level} {message}", serialize=True)
            logging.exception(f'Process.futures_listener: {e.status_code}, {e.message}')
            sys.exit(1)

    @LoguruDecoratorClass(level="INFO")
    async def activate(self):
        print_colored_and_boxed('Start listening...', 'RED')
        client = await AsyncClient.create()
        await self.futures_listener(client)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Process().activate())
