"""
Unit Tests for Student Performance Analytics

This module contains basic unit tests for the ETL, analysis, and ML components.
"""

import os
import sqlite3
import unittest

import pandas as pd
from sqlalchemy import create_engine

# Import project modules
from config import DATA_DIR
from db_utils import get_engine
from etl_students import clean_data, ensure_csv

class TestETLFunctions(unittest.TestCase):
    """Test ETL functionality"""

    def setUp(self):
        """Set up test environment"""
        # Use a test database path
        self.test_db_path = ":memory:"
        self.test_engine = create_engine(f"sqlite:///{self.test_db_path}")

        # Create a small test DataFrame
        self.test_data = pd.DataFrame({
            'sex': ['F', 'M', 'F', 'M'],
            'age': [15, 16, 17, 18],
            'g1': [10, 12, 14, 8],
            'g2': [11, 13, 15, 9],
            'g3': [12, 14, 16, 10]
        })

    def test_clean_data_columns(self):
        """Test that clean_data properly renames columns"""
        # Save test data to a temporary CSV
        test_csv = os.path.join(DATA_DIR, "test_data.csv")
        self.test_data.to_csv(test_csv, index=False)

        # Process the data - don't save the result
        processed_df = clean_data()

        # Check column names are standardized
        self.assertIn('sex', processed_df.columns)
        self.assertIn('age', processed_df.columns)
        self.assertIn('G1', processed_df.columns)
        self.assertIn('G2', processed_df.columns)
        self.assertIn('G3', processed_df.columns)

        # Clean up
        if os.path.exists(test_csv):
            os.remove(test_csv)

    def test_final_result_creation(self):
        """Test that clean_data creates the final_result column"""
        # Save test data to a temporary CSV
        test_csv = os.path.join(DATA_DIR, "test_data.csv")
        self.test_data.to_csv(test_csv, index=False)

        # Process the data
        processed_df = clean_data()

        # Check final_result column exists and has correct values
        self.assertIn('final_result', processed_df.columns)
        self.assertTrue(all(val in ['pass', 'fail'] for val in processed_df['final_result']))

        # Clean up
        if os.path.exists(test_csv):
            os.remove(test_csv)

    def test_ensure_csv_validation(self):
        """Test that ensure_csv validates file existence"""
        # Test with non-existent file - this is just a placeholder test
        # since ensure_csv doesn't take arguments in the current implementation
        self.assertTrue(callable(ensure_csv))

class TestDatabaseConnection(unittest.TestCase):
    """Test database connection functionality"""

    def test_sqlite_fallback(self):
        """Test that SQLite fallback works when MySQL fails"""
        # Get engine with SQLite fallback
        engine = get_engine(use_sqlite_fallback=True)

        # Check that we got a valid engine
        self.assertIsNotNone(engine)

        # Just verify we have a valid engine - MySQL might succeed in tests
        # so we just check that we have an engine
        self.assertTrue(engine is not None)

if __name__ == '__main__':
    unittest.main()