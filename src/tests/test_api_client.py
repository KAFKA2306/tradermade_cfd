import unittest
from unittest.mock import patch
import api_client

class TestApiClient(unittest.TestCase):
    @patch('api_client.tm.live')
    def test_get_real_time_data(self, mock_live):
        # Mock the tm.live function
        mock_live.return_value = [{'bid': 1.0, 'mid': 1.1, 'ask': 1.2}]
        # Call the function
        result = api_client.get_real_time_data('USOIL')
        # Assert the result
        self.assertEqual(result, [{'bid': 1.0, 'mid': 1.1, 'ask': 1.2}])
        mock_live.assert_called_once()

    @patch('api_client.tm.historical')
    def test_get_historical_data(self, mock_historical):
        # Mock the tm.historical function
        mock_historical.return_value = [{'open': 1.0, 'high': 1.2, 'low': 0.9, 'close': 1.1}]
        # Call the function
        result = api_client.get_historical_data('XAUUSD', '2024-01-01')
        # Assert the result
        self.assertEqual(result, [{'open': 1.0, 'high': 1.2, 'low': 0.9, 'close': 1.1}])
        mock_historical.assert_called_once()

    @patch('api_client.tm.timeseries')
    def test_get_time_series_data(self, mock_timeseries):
        # Mock the tm.timeseries function
        mock_timeseries.return_value = [{'open': 1.0, 'high': 1.2, 'low': 0.9, 'close': 1.1}]
        # Call the function
        result = api_client.get_time_series_data('UKOIL', '2024-01-01-00:00', '2024-01-01-01:00')
        # Assert the result
        self.assertEqual(result, [{'open': 1.0, 'high': 1.2, 'low': 0.9, 'close': 1.1}])
        mock_timeseries.assert_called_once()

if __name__ == '__main__':
    unittest.main()