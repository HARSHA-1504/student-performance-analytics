"""
Student Performance Analysis Module

This module provides functionality to export student performance summaries
for Power BI visualization and analysis.
"""

import logging
import pandas as pd
import os
from sqlalchemy import text
from db_utils import get_engine
from config import POWERBI_DIR, QUERIES

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def export_summaries():
    """
    Export student performance summaries to CSV files for Power BI.
    
    Exports:
    - Gender-based pass rate analysis
    - Age-based average grade analysis
    """
    try:
        eng = get_engine()
        
        # Gender-based pass rate analysis
        gender_query = text(QUERIES["gender_analysis"])
        df_gender = pd.read_sql(gender_query, eng)
        gender_file = os.path.join(POWERBI_DIR, "passrate_by_gender.csv")
        df_gender.to_csv(gender_file, index=False)
        logger.info(f"✅ Gender analysis exported to {gender_file}")
        
        # Age-based average grade analysis
        age_query = text(QUERIES["age_analysis"])
        df_age = pd.read_sql(age_query, eng)
        age_file = os.path.join(POWERBI_DIR, "avg_grade_by_age.csv")
        df_age.to_csv(age_file, index=False)
        logger.info(f"✅ Age analysis exported to {age_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error exporting summaries: {str(e)}")
        raise


if __name__ == "__main__":
    export_summaries()
