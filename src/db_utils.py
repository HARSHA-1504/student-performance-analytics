"""
Database Utilities Module

This module provides database connection utilities for the student performance
analytics project using MySQL and SQLAlchemy.
"""

import os
import logging
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Database configuration
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")


def get_engine(echo=False):
    """
    Create and return a SQLAlchemy database engine.
    
    Args:
        echo (bool): Whether to echo SQL statements (for debugging)
        
    Returns:
        sqlalchemy.engine.Engine: Database engine
        
    Raises:
        RuntimeError: If required database credentials are missing
    """
    try:
        # Validate required credentials
        if not DB_USER:
            raise RuntimeError("DB_USER not found in environment variables")
        if not DB_PASS:
            raise RuntimeError("DB_PASS not found in environment variables")
        if not DB_NAME:
            raise RuntimeError("DB_NAME not found in environment variables")
        
        # Construct connection string
        connection_string = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        
        # Create engine with connection pooling
        engine = create_engine(
            connection_string,
            echo=echo,
            pool_pre_ping=True,
            pool_recycle=3600,  # Recycle connections every hour
            pool_size=5,        # Number of connections to maintain
            max_overflow=10     # Additional connections beyond pool_size
        )
        
        logger.info(f"✅ Database engine created for {DB_NAME} on {DB_HOST}:{DB_PORT}")
        return engine
        
    except Exception as e:
        logger.error(f"❌ Error creating database engine: {str(e)}")
        raise


def test_connection():
    """
    Test the database connection.
    
    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        engine = get_engine()
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        logger.info("✅ Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {str(e)}")
        return False
