"""
Student Performance Analysis Module

This module provides functionality to export student performance summaries
for Power BI visualization and analysis.
"""

import os
import logging
import pandas as pd
from db_utils import get_engine

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Constants
ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "powerbi")
os.makedirs(OUT, exist_ok=True)


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
        gender_query = """
        SELECT sex, final_result, COUNT(*) AS count
        FROM students
        GROUP BY sex, final_result
        ORDER BY sex, final_result;
        """
        
        df_gender = pd.read_sql(gender_query, eng)
        gender_file = os.path.join(OUT, "passrate_by_gender.csv")
        df_gender.to_csv(gender_file, index=False)
        logger.info(f"✅ Gender analysis exported to {gender_file}")
        
        # Age-based average grade analysis
        age_query = """
        SELECT age, ROUND(AVG(G3), 2) AS avg_final
        FROM students
        GROUP BY age 
        ORDER BY age;
        """
        
        df_age = pd.read_sql(age_query, eng)
        age_file = os.path.join(OUT, "avg_grade_by_age.csv")
        df_age.to_csv(age_file, index=False)
        logger.info(f"✅ Age analysis exported to {age_file}")
        
        return True
        
    except Exception as e:
        logger.error(f"❌ Error exporting summaries: {str(e)}")
        raise


if __name__ == "__main__":
    export_summaries()
