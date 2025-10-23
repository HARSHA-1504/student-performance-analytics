@echo off
cd /d "C:\Users\reddy\OneDrive\Desktop\student-performance-analytics"
call .venv\Scripts\activate
python src\etl_students.py
exit
