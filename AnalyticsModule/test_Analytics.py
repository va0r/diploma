import unittest
from unittest.mock import patch

from AnalyticsModule.code import AnalyticsClass


class TestAnalyticsClass(unittest.TestCase):

    @patch('AnalyticsModule.code.Client')
    @patch('AnalyticsModule.code.PostgresDBClass')
    def test_get_data(self, mock_client, mock_db):
        # Instantiate AnalyticsClass
        analytics = AnalyticsClass(interval='1h', days=30)

        # Prepare mocked data
        mock_client.return_value.futures_historical_klines.side_effect = [
            [["2024-01-16 00:00:00.000", "42515", "42597", "42466.1", "42572.3", "1427.488",
              "2024-01-16 00:14:59.999", "60713678.6472", 25408, "745.83", "31720517.404", 0],
             ["2024-01-16 00:15:00.000", "42572.4", "42656", "42532.6", "42642.9", "1352.691",
              "2024-01-16 00:29:59.999", "57641439.6829", 21317, "818.395", "34875667.4327", 0]],
            [["2024-01-16 00:00:00.000", "2512.2", "2516.97", "2511.5", "2512.44", "13752.617",
              "2024-01-16 00:14:59.999", "34568761.39166", 23257, "6716.053", "16881280.91921", 0],
             ["2024-01-16 00:15:00.000", "2512.44", "2516.78", "2507.33", "2513.94", "18214.844",
              "2024-01-16 00:29:59.999", "45755582.78274", 27593, "9148.042", "22981764.82937", 0]]
        ]

        # Call get_data method
        x, y = analytics.get_data()

        # Assert the returned values
        self.assertEqual(x, [4, 10])
        self.assertEqual(y, [18, 24])

        # Assert that PostgresDBClass was called
        mock_db.return_value.load_dataframe.assert_called()

    @patch('AnalyticsModule.code.stats')
    @patch('AnalyticsModule.code.AnalyticsClass.get_data', return_value=([1, 2, 3], [4, 5, 6]))
    def test_create_coefficients(self, mock_get_data, mock_stats):
        # Instantiate AnalyticsClass
        analytics = AnalyticsClass(interval='1h', days=30)

        # Mock the linregress method
        mock_stats.linregress.return_value = (2, 1, 0, 0, 0.5)

        # Call create_coefficients method
        slope, intercept = analytics.create_coefficients()

        # Assert the returned values
        self.assertEqual(slope, 2)
        self.assertEqual(intercept, 1)


if __name__ == '__main__':
    unittest.main()
