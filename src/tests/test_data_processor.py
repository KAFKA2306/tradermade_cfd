import unittest
import pandas as pd
import os
import data_processor
import config
from unittest.mock import patch
from datetime import datetime

class TestDataProcessor(unittest.TestCase):

    @patch('src.data_processor.datetime')
    def test_save_data_parquet_dataframe(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample DataFrame
        data = pd.DataFrame({'col1': [1, 2], 'col2': [3, 4]})
        filename_prefix = "test_data"
        data_dir = "test_dir"

        # Call the function
        filepath = data_processor._save_data_parquet(data, filename_prefix, data_dir)

        # Assert that the file was created
        self.assertTrue(os.path.exists(filepath))

        # Clean up the created file and directory
        os.remove(filepath)
        os.rmdir(data_dir)

    @patch('src.data_processor.datetime')
    def test_save_data_parquet_dict_with_quotes(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample dictionary with 'quotes'
        data = {'quotes': [{'col1': 1, 'col2': 2}, {'col1': 3, 'col2': 4}]}
        filename_prefix = "test_data"
        data_dir = "test_dir"

        # Call the function
        filepath = data_processor._save_data_parquet(data, filename_prefix, data_dir)

        # Assert that the file was created
        self.assertTrue(os.path.exists(filepath))

        # Clean up the created file and directory
        os.remove(filepath)
        os.rmdir(data_dir)

    @patch('src.data_processor.datetime')
    def test_save_data_parquet_empty_quotes(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample dictionary with empty 'quotes'
        data = {'quotes': []}
        filename_prefix = "test_data"
        data_dir = "test_dir"

        # Call the function
        filepath = data_processor._save_data_parquet(data, filename_prefix, data_dir)

        # Assert that the function returns None
        self.assertIsNone(filepath)

    @patch('src.data_processor.datetime')
    def test_save_data_parquet_api_error(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample dictionary representing an API error
        data = {'message': 'API error occurred'}
        filename_prefix = "test_data"
        data_dir = "test_dir"

        # Call the function
        filepath = data_processor._save_data_parquet(data, filename_prefix, data_dir)

        # Assert that the function returns None
        self.assertIsNone(filepath)

    @patch('src.data_processor.datetime')
    def test_save_data_parquet_empty_list(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create an empty list
        data = []
        filename_prefix = "test_data"
        data_dir = "test_dir"

        # Call the function
        filepath = data_processor._save_data_parquet(data, filename_prefix, data_dir)

        # Assert that the function returns None
        self.assertIsNone(filepath)

    @patch('src.data_processor.datetime')
    def test_save_data_parquet_other_dict(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample dictionary
        data = {'col1': 1, 'col2': 2}
        filename_prefix = "test_data"
        data_dir = "test_dir"

        # Call the function
        filepath = data_processor._save_data_parquet(data, filename_prefix, data_dir)

        # Assert that the file was created
        self.assertTrue(os.path.exists(filepath))

        # Clean up the created file and directory
        os.remove(filepath)
        os.rmdir(data_dir)

    @patch('src.data_processor.datetime')
    def test_save_real_time_data(self, mock_datetime):
        # Mock datetime to have a consistent filename
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample real-time data
        data = [{'col1': 1, 'col2': 2}, {'col1': 3, 'col2': 4}]

        # Call the function
        filepath = data_processor.save_real_time_data(data)

        # Assert that the file was created
        self.assertTrue(os.path.exists(filepath))

        # Read the data back from the file
        read_data = pd.read_parquet(filepath)

        # Assert that the data is the same as the original
        self.assertTrue(read_data.equals(pd.DataFrame(data)))

        # Clean up the created file and directory
        os.remove(filepath)
        # config.REAL_TIME_DIR が存在しない場合があるので、try-except で囲む
        try:
            os.rmdir(config.REAL_TIME_DIR)
        except OSError:
            pass

    @patch('src.data_processor.datetime')
    def test_save_historical_data(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample historical data
        data = {'col1': 1, 'col2': 2}

        # Call the function
        filepath = data_processor.save_historical_data(data)

        # Assert that the file was created
        self.assertTrue(os.path.exists(filepath))

        # Read the data back from the file
        read_data = pd.read_parquet(filepath)

        # Assert that the data is the same as the original
        self.assertTrue(read_data.equals(pd.DataFrame([data])))

        # Clean up the created file and directory
        os.remove(filepath)
        # config.HISTORICAL_DIR が存在しない場合があるので、try-except で囲む
        try:
            os.rmdir(config.HISTORICAL_DIR)
        except OSError:
            pass

    @patch('src.data_processor.datetime')
    def test_save_time_series_data(self, mock_datetime):
        # Mock datetime to have a consistent filename
        mock_datetime.now.return_value = datetime(2023, 1, 1, 0, 0, 0)

        # Create a sample time series data
        data = {'quotes': [{'col1': 1, 'col2': 2}, {'col1': 3, 'col2': 4}]}

        # Call the function
        filepath = data_processor.save_time_series_data(data)

        # Assert that the file was created
        self.assertTrue(os.path.exists(filepath))

        # Read the data back from the file
        read_data = pd.read_parquet(filepath)

        # Assert that the data is the same as the original
        self.assertTrue(read_data.equals(pd.DataFrame(data['quotes'])))

        # Clean up the created file and directory
        os.remove(filepath)
        # config.TIME_SERIES_DIR が存在しない場合があるので、try-except で囲む
        try:
            os.rmdir(config.TIME_SERIES_DIR)
        except OSError:
            pass

if __name__ == '__main__':
    unittest.main()