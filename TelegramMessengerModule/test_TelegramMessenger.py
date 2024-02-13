import unittest
from unittest.mock import patch

from TelegramMessengerModule.code import TelegramMessengerClass


class TestTelegramMessenger(unittest.TestCase):

    @patch('aiohttp.ClientSession.post')  # Mock the post request
    def test_send_message_success(self, mock_post):
        mock_post.return_value.__aenter__.return_value.json.return_value = {'ok': True}
        messenger = TelegramMessengerClass('fake_token')

        result = messenger.send_message(12345, 'Hello!')

        self.assertTrue(result.get('ok'))  # Assert successful response
        mock_post.assert_called_once_with('https://api.telegram.org/...', data={'chat_id': 12345, 'text': 'Hello!'})

    @patch('aiohttp.ClientSession.post')  # Mock the post request
    def test_send_message_error(self, mock_post):
        mock_post.return_value.__aenter__.return_value.json.return_value = {'ok': False, 'error_code': 400}
        messenger = TelegramMessengerClass('fake_token')

        with self.assertRaises(Exception):  # Expect an exception
            messenger.send_message(12345, 'Invalid Message')

        mock_post.assert_called_once_with('https://api.telegram.org/...',
                                          data={'chat_id': 12345, 'text': 'Invalid Message'})


if __name__ == '__main__':
    unittest.main()
