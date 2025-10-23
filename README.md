# Student Performance Analytics

A comprehensive data pipeline for analyzing student performance data, including ETL processes, database storage, analysis exports, and machine learning predictions.

## Features

- **ETL Pipeline**: Clean and process student data from CSV files
- **Database Storage**: Store processed data in MySQL with SQLite fallback
- **Analysis Exports**: Generate summary reports for Power BI visualization
- **Machine Learning**: Predict student pass/fail outcomes using Random Forest

## Setup

### Prerequisites

- Python 3.7+
- MySQL (optional - SQLite fallback available)
- Required Python packages (see requirements.txt)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/student-performance-analytics.git
   cd student-performance-analytics
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Configure database settings:
   ```
   cp env.example .env
   ```
   Edit the `.env` file with your database credentials.

## Usage

### ETL Process

Process the raw student data:
```
python src/etl_students.py
```

### Generate Analysis Reports

Create summary reports for Power BI:
```
python src/analysis_students.py
```

### Train and Evaluate ML Model

Train the pass/fail prediction model:
```
python src/ml_predict_passfail.py
```

### Run Tests

Execute unit tests:
```
python src/test_setup.py
```

## Project Structure

- `src/` - Source code
  - `config.py` - Centralized configuration
  - `db_utils.py` - Database connection utilities
  - `etl_students.py` - ETL processing
  - `analysis_students.py` - Analysis exports
  - `ml_predict_passfail.py` - Machine learning module
  - `test_setup.py` - Unit tests
- `data/` - Data files
  - `raw/` - Raw CSV data
  - `processed/` - Processed data
- `powerbi/` - Power BI export files
- `models/` - Saved ML models

## Database Support

The system supports both MySQL and SQLite:
- MySQL is used by default when credentials are provided in `.env`
- SQLite is used as a fallback when MySQL connection fails

## License

[MIT License](LICENSE)