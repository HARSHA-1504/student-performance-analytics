"""
Configuration Module

This module centralizes configuration settings for the student performance analytics project.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Project paths
ROOT_DIR = os.path.join(os.path.dirname(__file__), "..")
DATA_DIR = os.path.join(ROOT_DIR, "data")
POWERBI_DIR = os.path.join(ROOT_DIR, "powerbi")

# Ensure directories exist
os.makedirs(DATA_DIR, exist_ok=True)
os.makedirs(POWERBI_DIR, exist_ok=True)

# Data files
CSV_FILE = os.path.join(DATA_DIR, "student-mat.csv")
PROCESSED_FILE = os.path.join(DATA_DIR, "students_processed.csv")
MODEL_FILE = os.path.join(DATA_DIR, "passfail_model.pkl")

# Database configuration
DB_CONFIG = {
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASS"),
    "host": os.getenv("DB_HOST", "127.0.0.1"),
    "port": os.getenv("DB_PORT", "3306"),
    "database": os.getenv("DB_NAME"),
    "pool_size": int(os.getenv("DB_POOL_SIZE", "5")),
    "max_overflow": int(os.getenv("DB_MAX_OVERFLOW", "10")),
    "pool_recycle": int(os.getenv("DB_POOL_RECYCLE", "3600")),
}

# SQLite fallback configuration
SQLITE_DB_PATH = os.path.join(DATA_DIR, "student_analytics.db")

# ML model configuration
ML_CONFIG = {
    "features": ['studytime', 'failures', 'absences', 'G1', 'G2'],
    "target": "final_result",
    "test_size": 0.2,
    "random_state": 42,
}

# SQL queries
QUERIES = {
    "gender_analysis": """
    SELECT sex, final_result, COUNT(*) AS count
    FROM students
    GROUP BY sex, final_result
    ORDER BY sex, final_result;
    """,
    
    "age_analysis": """
    SELECT age, ROUND(AVG(G3), 2) AS avg_final
    FROM students
    GROUP BY age
    ORDER BY age;
    """,
}