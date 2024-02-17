import unittest
from unittest.mock import patch, MagicMock

import pandas as pd

from PostgresDBModule.code import PostgresDBClass


class TestPostgresDBClass(unittest.TestCase):
    def setUp(self):
        # Устанавливаем переменную среды для POSTGRES_ACCESS_LINE
        self.patcher = patch.dict('os.environ', {'POSTGRES_ACCESS_LINE': 'postgres:ghjcnjq77@localhost:5432/diploma'})
        self.patcher.start()

        # Создаем экземпляр PostgresDBClass
        self.postgres_instance = PostgresDBClass()

    def tearDown(self):
        # Останавливаем патчер
        self.patcher.stop()

    def test_load_dataframe(self):
        existing_df = pd.DataFrame({'datetime': ['2024-01-01 12:00:00']})
        existing_df['datetime'] = pd.to_datetime(existing_df['datetime'])
        with patch('PostgresDBModule.code.create_engine') as mock_create_engine, \
                patch('PostgresDBModule.code.MetaData') as mock_meta_data:
            mock_engine_instance = MagicMock()
            mock_create_engine.return_value = mock_engine_instance
            mock_metadata_instance = MagicMock()
            mock_meta_data.return_value = mock_metadata_instance

            test_dataframe = pd.DataFrame({'col1': [1, 2, 3]})
            with patch('PostgresDBModule.code.pd.read_sql') as mock_read_sql, \
                    patch('PostgresDBModule.code.pd.Timestamp.now') as mock_now:
                mock_now.return_value = pd.Timestamp('2024-02-17 15:00:00')
                mock_read_sql.return_value = existing_df

                # Testing for SESSION table
                self.postgres_instance.load_dataframe(test_dataframe, 'SESSION')
                mock_read_sql.assert_called_once_with('SESSION', mock_engine_instance, columns=['datetime'])
                mock_create_engine.assert_called()

                # Testing for non-SESSION table
                self.postgres_instance.load_dataframe(test_dataframe, 'OTHER_TABLE')
                mock_create_engine.assert_called()

                # Testing for SESSION table with existing table and recent datetime
                self.postgres_instance.load_dataframe(test_dataframe, 'SESSION')
                mock_read_sql.assert_called_with('SESSION', mock_engine_instance, columns=['datetime'])
                mock_create_engine.assert_called()

                # Testing for SESSION table with existing table and old datetime
                mock_read_sql.return_value = pd.DataFrame({'datetime': ['2024-01-01 12:00:00']})
                self.postgres_instance.load_dataframe(test_dataframe, 'SESSION')
                mock_read_sql.assert_called_with('SESSION', mock_engine_instance, columns=['datetime'])
                mock_create_engine.assert_called()


if __name__ == '__main__':
    unittest.main()
