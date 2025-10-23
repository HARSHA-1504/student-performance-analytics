#!/usr/bin/env python3
"""
Project Setup Test Script

This script validates that all required dependencies and configurations
are properly set up for the student performance analytics project.
"""

import sys
import os
import importlib
from pathlib import Path

def test_imports():
    """Test that all required packages can be imported."""
    required_packages = [
        'pandas',
        'numpy', 
        'sklearn',
        'sqlalchemy',
        'mysql.connector',
        'dotenv',
        'joblib',
        'matplotlib',
        'seaborn',
        'jupyter'
    ]
    
    print("Testing package imports...")
    failed_imports = []
    
    for package in required_packages:
        try:
            importlib.import_module(package)
            print(f"[OK] {package}")
        except ImportError as e:
            print(f"[ERROR] {package}: {e}")
            failed_imports.append(package)
    
    return failed_imports

def test_project_structure():
    """Test that the project structure is correct."""
    print("\nTesting project structure...")
    
    required_dirs = ['src', 'data', 'notebooks', 'powerbi']
    required_files = [
        'src/analysis_students.py',
        'src/etl_students.py', 
        'src/ml_predict_passfail.py',
        'src/db_utils.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    missing_items = []
    
    for directory in required_dirs:
        if not os.path.exists(directory):
            print(f"[ERROR] Missing directory: {directory}")
            missing_items.append(directory)
        else:
            print(f"[OK] {directory}/")
    
    for file_path in required_files:
        if not os.path.exists(file_path):
            print(f"[ERROR] Missing file: {file_path}")
            missing_items.append(file_path)
        else:
            print(f"[OK] {file_path}")
    
    return missing_items

def test_environment():
    """Test environment configuration."""
    print("\nTesting environment configuration...")
    
    # Check if .env file exists
    env_file = '.env'
    if not os.path.exists(env_file):
        print(f"[WARNING] {env_file} not found. Please copy env.example to .env and configure it.")
        return False
    
    print(f"[OK] {env_file} found")
    
    # Test database connection (if .env is configured)
    try:
        from src.db_utils import test_connection
        if test_connection():
            print("[OK] Database connection successful")
        else:
            print("[WARNING] Database connection failed - check your .env configuration")
    except Exception as e:
        print(f"[WARNING] Database connection test failed: {e}")
    
    return True

def main():
    """Run all tests."""
    print("=" * 60)
    print("STUDENT PERFORMANCE ANALYTICS - SETUP VALIDATION")
    print("=" * 60)
    
    # Test imports
    failed_imports = test_imports()
    
    # Test project structure
    missing_items = test_project_structure()
    
    # Test environment
    env_ok = test_environment()
    
    # Summary
    print("\n" + "=" * 60)
    print("SETUP VALIDATION SUMMARY")
    print("=" * 60)
    
    if failed_imports:
        print(f"[ERROR] Failed imports: {', '.join(failed_imports)}")
        print("   Run: pip install -r requirements.txt")
    else:
        print("[OK] All required packages imported successfully")
    
    if missing_items:
        print(f"[ERROR] Missing items: {', '.join(missing_items)}")
    else:
        print("[OK] Project structure is complete")
    
    if not env_ok:
        print("[WARNING] Environment configuration needs attention")
    else:
        print("[OK] Environment configuration looks good")
    
    if not failed_imports and not missing_items and env_ok:
        print("\n[SUCCESS] Project setup is complete and ready to use!")
        print("\nNext steps:")
        print("1. Place student-mat.csv in the data/ directory")
        print("2. Run: python src/etl_students.py")
        print("3. Run: python src/ml_predict_passfail.py")
        print("4. Run: python src/analysis_students.py")
        return True
    else:
        print("\n[WARNING] Please fix the issues above before proceeding")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
