from loguru import logger


class LoguruDecoratorClass:
    def __init__(self, level="INFO"):
        self.level = level

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            logger.add("logfile.log", level=self.level)  # Установка уровня логирования
            logger.log(self.level, f"Вызов функции {func.__name__} с аргументами: {args}, {kwargs}")
            result = func(*args, **kwargs)
            logger.log(self.level, f"Результат выполнения функции {func.__name__}: {result}")
            return result

        return wrapper
