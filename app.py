import asyncio
import logging
import sys
from datetime import datetime

from binance import AsyncClient, BinanceSocketManager
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv, find_dotenv

from Application.code import Application

load_dotenv(find_dotenv())


class Process(Application):
    """
    Asynchronously retrieve and process current data.
    """

    async def futures_listener(self, client):
        """
        The coroutine to infinitely retrieve and set the current BTCUSDT and ETHUSDT price
        and time data from the websocket stream and then call the processing coroutine.
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
            logging.exception(f'Process.futures_listener: {e.status_code}, {e.message}')
            sys.exit(1)

    async def activate(self):
        print('Start listening...')
        client = await AsyncClient.create()
        await self.futures_listener(client)


if __name__ == "__main__":

    # TODO удалить все данные из таблицы SESSION

    loop = asyncio.get_event_loop()
    loop.run_until_complete(Process().activate())
