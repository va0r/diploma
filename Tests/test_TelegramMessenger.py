import os
import unittest
from unittest.mock import patch, AsyncMock

from dotenv import load_dotenv, find_dotenv

from TelegramMessengerModule.code import TelegramMessengerClass

load_dotenv(find_dotenv())


class TestTelegramMessengerClass(unittest.IsolatedAsyncioTestCase):
    @patch('TelegramMessengerModule.code.aiohttp.ClientSession.post')
    async def test_send_message(self, mock_post):
        mock_response = {'status': 'success'}
        mock_post.return_value.__aenter__.return_value.json = AsyncMock(return_value=mock_response)

        token = os.getenv('BOT_TOKEN')
        telegram_id = os.getenv('TELEGRAM_ID')
        message = "Test message"

        telegram = TelegramMessengerClass(token)
        response = await telegram.send_message(telegram_id, message)

        self.assertEqual(response, mock_response)
        mock_post.assert_called_once_with(
            f"https://api.telegram.org/bot{token}/sendMessage",
            data={"chat_id": telegram_id, "text": message}
        )


if __name__ == '__main__':
    unittest.main()
