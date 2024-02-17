import unittest
from unittest.mock import patch

import numpy as np
import pandas as pd
from sqlalchemy import create_engine

from PostgresDBModule.code import PostgresDBClass


class TestPostgresDBClass(unittest.TestCase):

    def setUp(self):
        self.postgres_instance = PostgresDBClass()

    def test_initialization(self):
        self.assertIsInstance(self.postgres_instance, PostgresDBClass)

    def test_load_dataframe(self):
        # Подготовка тестовых данных
        test_df = pd.DataFrame(np.array([['2024-02-02 02:02:02.002', 2000, 50000, 60, 1.15]]),
                               columns=['datetime', 'ethusdt', 'btcusdt', 'ethusdt_decoupled', 'percentage'])
        table_name = 'table'

        # Загрузка данных в таблицу
        self.postgres_instance.load_dataframe(test_df, table_name)

        # Проверка наличия данных в таблице
        engine = create_engine(self.postgres_instance.postgres_url)
        loaded_df = pd.read_sql(table_name, engine)
        self.assertIsNotNone(loaded_df)

    @patch('PostgresDBModule.code.os.getenv')
    def test_init_raises_value_error(self, mock_getenv):
        mock_getenv.return_value = None

        with self.assertRaises(ValueError):
            PostgresDBClass()


if __name__ == '__main__':
    unittest.main()
