import unittest

import pandas as pd
from sqlalchemy import create_engine

from PostgresDBModule.code import PostgresDBClass


class TestPostgresDBClass(unittest.TestCase):

    def setUp(self):
        self.postgres_instance = PostgresDBClass()

    def test_initialization(self):
        self.assertIsInstance(self.postgres_instance, PostgresDBClass)

    def test_load_dataframe_existing_table(self):
        # Подготовка тестовых данных
        test_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        table_name = 'existing_table'

        # Загрузка данных в существующую таблицу
        self.postgres_instance.load_dataframe(test_df, table_name)

        # Проверка наличия данных в таблице
        engine = create_engine(self.postgres_instance.postgres_url)
        loaded_df = pd.read_sql(table_name, engine)
        self.assertFalse(loaded_df.empty)

    def test_load_dataframe_new_table(self):
        # Подготовка тестовых данных
        test_df = pd.DataFrame({'col1': [1, 2, 3], 'col2': ['a', 'b', 'c']})
        table_name = 'new_table'

        # Загрузка данных в новую таблицу
        self.postgres_instance.load_dataframe(test_df, table_name)

        # Проверка наличия данных в таблице
        engine = create_engine(self.postgres_instance.postgres_url)
        loaded_df = pd.read_sql(table_name, engine)
        self.assertFalse(loaded_df.empty)


if __name__ == '__main__':
    unittest.main()
