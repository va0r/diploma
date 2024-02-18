import os

from loguru import logger


class LoguruDecoratorClass:
    """
    Класс для логирования работы приложения.
    Использует пакет loguru для записи лог-файла в формате json.
    """
    def __init__(self, level="INFO", rotation="24h", serializer=True):
        self.level = level
        self.rotation = rotation
        self.serializer = serializer

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            logfile_path = os.path.join(os.getcwd(), "logfile.json")
            logger.add(logfile_path,
                       level=self.level,
                       rotation=self.rotation,
                       serialize=self.serializer)
            logger.log(self.level, f"Вызов функции {func.__name__} с аргументами: {args = }, {kwargs = }")
            result = func(*args, **kwargs)
            logger.log(self.level, f"Результат выполнения функции {func.__name__}: {result = }")
            return result

        return wrapper
