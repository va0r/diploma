import aiohttp

from LoguruModule.code import LoguruDecoratorClass


class TelegramMessengerClass:
    """
    Класс для работы с тг-ботом.
    Реализует функционал отправки сообщения через тг-бот.
    """
    def __init__(self, token):
        self.token = token
        self.url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    @LoguruDecoratorClass(level="INFO")
    async def send_message(self, telegram_id, message):
        data = {
            "chat_id": telegram_id,
            "text": message,
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(self.url, data=data) as response:
                return await response.json()
