import unittest
from datetime import datetime, timedelta
from unittest.mock import patch

import numpy as np
import pandas as pd

from PostgresDBModule.code import PostgresDBClass


class TestTablesPostgresDBClass(unittest.TestCase):
    def setUp(self):
        self.postgres_instance = PostgresDBClass()
        test_df = pd.DataFrame(np.array([['2024-02-02 02:02:02.002', 2000, 50000, 60, 1.15]]),
                               columns=['datetime', 'ethusdt', 'btcusdt', 'ethusdt_decoupled', 'percentage'])
        test_df = test_df.astype({'datetime': 'datetime64[ns]',
                                   'ethusdt': float,
                                   'btcusdt': float,
                                   'ethusdt_decoupled': float,
                                   'percentage': float})
        self.test_dataframe = test_df

    @patch('pandas.read_sql', return_value=pd.DataFrame({'datetime': [datetime.now() - timedelta(hours=2)]}))
    def test_load_dataframe_session_existing_append(self, mock_read_sql):
        table_name = 'SESSION'
        self.postgres_instance.metadata.tables = {'SESSION': 'example_table'}
        self.postgres_instance.load_dataframe(self.test_dataframe, table_name)
        mock_read_sql.assert_called_once_with(table_name, self.postgres_instance.engine, columns=['datetime'])
        self.assertEqual(mock_read_sql.call_count, 1)

    @patch('pandas.read_sql', return_value=pd.DataFrame({'datetime': [datetime.now() - timedelta(hours=2)]}))
    def test_load_dataframe_session_existing_replace(self, mock_read_sql):
        table_name = 'SESSION'
        self.postgres_instance.metadata.tables = {'SESSION': 'example_table'}
        self.postgres_instance.load_dataframe(self.test_dataframe, table_name, if_exists='replace')
        mock_read_sql.assert_called_once_with(table_name, self.postgres_instance.engine, columns=['datetime'])
        self.assertEqual(mock_read_sql.call_count, 1)

    @patch('pandas.read_sql', return_value=pd.DataFrame())
    def test_load_dataframe_session_non_existing(self, mock_read_sql):
        table_name = 'SESSION'
        self.postgres_instance.metadata.tables = {}
        self.postgres_instance.load_dataframe(self.test_dataframe, table_name)
        mock_read_sql.assert_not_called()

    def test_load_dataframe_non_session(self):
        table_name = 'OTHER_TABLE'
        self.postgres_instance.metadata.tables = {}
        self.postgres_instance.load_dataframe(self.test_dataframe, table_name)


class TestLineAccessPostgresDBClass(unittest.TestCase):

    def setUp(self):
        self.postgres_instance = PostgresDBClass()

    def test_initialization(self):
        self.assertIsInstance(self.postgres_instance, PostgresDBClass)

    @patch('PostgresDBModule.code.os.getenv', return_value=None)
    def test_init_raises_value_error(self, mock_getenv):
        with self.assertRaises(ValueError):
            PostgresDBClass()


if __name__ == '__main__':
    unittest.main()
