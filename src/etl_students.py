"""
Student Performance ETL Module

This module handles the Extract, Transform, and Load (ETL) process
for student performance data from CSV to MySQL database.
"""

import os
import logging
import pandas as pd
from sqlalchemy import text
from db_utils import get_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
ROOT = os.path.join(os.path.dirname(__file__), "..")
DATA = os.path.join(ROOT, "data")
os.makedirs(DATA, exist_ok=True)

CSV_FILE = os.path.join(DATA, "student-mat.csv")
PROCESSED = os.path.join(DATA, "students_processed.csv")


def ensure_csv():
    """
    Verify that the source CSV file exists.
    
    Raises:
        FileNotFoundError: If the CSV file is not found
    """
    if not os.path.exists(CSV_FILE):
        error_msg = f"❌ File not found: {CSV_FILE}\nDownload from UCI and place it in /data."
        logger.error(error_msg)
        raise FileNotFoundError(error_msg)
    logger.info(f"✅ Found dataset: {CSV_FILE}")


def clean_data():
    """
    Clean and preprocess the student data.
    
    Returns:
        pd.DataFrame: Cleaned and processed dataframe
    """
    try:
        # Load data
        df = pd.read_csv(CSV_FILE, sep=';')
        logger.info(f"Loaded {len(df)} rows from {CSV_FILE}")
        
        # Clean column names
        df.columns = [col.strip() for col in df.columns]
        
        # Process grade columns (G1, G2, G3)
        grade_columns = ['G1', 'G2', 'G3']
        for col in grade_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0).astype(int)
                logger.info(f"Processed {col} column")
        
        # Create pass/fail target variable
        df['final_result'] = df['G3'].apply(lambda x: 'pass' if x >= 10 else 'fail')
        
        # Save processed data
        df.to_csv(PROCESSED, index=False)
        logger.info(f"✅ Cleaned data saved → {PROCESSED}")
        
        return df
        
    except Exception as e:
        logger.error(f"❌ Error cleaning data: {str(e)}")
        raise


def load_mysql(df):
    """
    Load processed data into MySQL database.
    
    Args:
        df (pd.DataFrame): Processed dataframe to load
    """
    try:
        eng = get_engine()
        
        # Load data to MySQL
        df.to_sql(
            "students", 
            eng, 
            if_exists="replace", 
            index=False, 
            chunksize=2000, 
            method="multi"
        )
        logger.info("Data loaded to MySQL table: students")
        
        # Add index for performance
        with eng.connect() as conn:
            try:
                conn.execute(text("ALTER TABLE students ADD INDEX idx_final_result (final_result(10))"))
                logger.info("✅ Index added to final_result column")
            except Exception as e:
                logger.warning(f"⚠️ Index may already exist: {e}")
        
        logger.info("✅ Data successfully loaded to MySQL")
        
    except Exception as e:
        logger.error(f"❌ Error loading data to MySQL: {str(e)}")
        raise


def main():
    """
    Main ETL process execution.
    """
    try:
        ensure_csv()
        df = clean_data()
        load_mysql(df)
        logger.info(f"🎯 ETL finished successfully. Rows processed: {len(df)}")
        
    except Exception as e:
        logger.error(f"❌ ETL process failed: {str(e)}")
        raise


if __name__ == "__main__":
    main()
