"""
Database Utilities Module

This module provides database connection utilities for the student performance
analytics project using MySQL and SQLAlchemy.
"""

import os
import logging
import sqlalchemy
from sqlalchemy import create_engine, text
from config import DB_CONFIG, SQLITE_DB_PATH

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def get_engine(echo=False, use_sqlite_fallback=True):
    """
    Create and return a SQLAlchemy database engine.
    
    Args:
        echo (bool): Whether to echo SQL statements (for debugging)
        use_sqlite_fallback (bool): Whether to use SQLite as fallback if MySQL fails
        
    Returns:
        sqlalchemy.engine.Engine: Database engine
        
    Raises:
        RuntimeError: If required database credentials are missing and fallback is disabled
    """
    try:
        # Validate required credentials
        if not DB_CONFIG["user"]:
            raise RuntimeError("DB_USER not found in environment variables")
        if not DB_CONFIG["password"]:
            raise RuntimeError("DB_PASS not found in environment variables")
        if not DB_CONFIG["database"]:
            raise RuntimeError("DB_NAME not found in environment variables")
        
        # Construct connection string
        connection_string = (
            f"mysql+mysqlconnector://{DB_CONFIG['user']}:{DB_CONFIG['password']}@"
            f"{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}"
        )
        
        # Create engine with connection pooling
        engine = create_engine(
            connection_string,
            echo=echo,
            pool_pre_ping=True,
            pool_recycle=DB_CONFIG["pool_recycle"],
            pool_size=DB_CONFIG["pool_size"],
            max_overflow=DB_CONFIG["max_overflow"]
        )
        
        # Test connection properly with text() wrapper
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        
        logger.info(f"✅ Database engine created for {DB_CONFIG['database']} on {DB_CONFIG['host']}:{DB_CONFIG['port']}")
        return engine
    except Exception as e:
        if use_sqlite_fallback:
            logger.warning(f"⚠️ MySQL connection failed: {str(e)}. Using SQLite fallback.")
            sqlite_engine = create_engine(f"sqlite:///{SQLITE_DB_PATH}", echo=echo)
            logger.info(f"✅ SQLite fallback engine created at {SQLITE_DB_PATH}")
            return sqlite_engine
        else:
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
            conn.execute(text("SELECT 1"))
        logger.info("✅ Database connection test successful")
        return True
    except Exception as e:
        logger.error(f"❌ Database connection test failed: {str(e)}")
        return False
