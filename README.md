# Student Performance Analytics

A Python-based data analytics project for analyzing student performance using machine learning and data visualization.

## 📊 Project Overview

This project analyzes student performance data to predict pass/fail outcomes and generate insights through:
- **ETL Pipeline**: Data extraction, transformation, and loading into MySQL database
- **Machine Learning**: Random Forest classifier for pass/fail prediction
- **Data Visualization**: Power BI dashboards and CSV exports for analysis

## 🏗️ Project Structure

```
student-performance-analytics/
├── data/                          # Data storage
│   ├── student-mat.csv           # Original dataset
│   ├── students_processed.csv    # Cleaned dataset
│   └── passfail_model.pkl       # Trained ML model
├── notebooks/                     # Jupyter notebooks
│   └── EDA.ipynb                # Exploratory Data Analysis
├── powerbi/                      # Power BI files and exports
│   ├── Student_Performance.pbix  # Power BI dashboard
│   ├── avg_grade_by_age.csv     # Age-based grade analysis
│   └── passrate_by_gender.csv   # Gender-based pass rate analysis
├── src/                          # Source code
│   ├── analysis_students.py     # Data analysis and export
│   ├── db_utils.py              # Database utilities
│   ├── etl_students.py          # ETL pipeline
│   └── ml_predict_passfail.py   # Machine learning model
├── requirements.txt              # Python dependencies
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- MySQL Server

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/HARSHA-1504/student-performance-analytics.git
   cd student-performance-analytics
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the project root:
   ```env
   DB_USER=your_mysql_username
   DB_PASS=your_mysql_password
   DB_HOST=127.0.0.1
   DB_PORT=3306
   DB_NAME=student_analytics
   ```

5. **Set up MySQL database**
   ```sql
   CREATE DATABASE student_analytics;
   ```

6. **Download the dataset**
   - Download `student-mat.csv` from the UCI Machine Learning Repository
   - Place it in the `data/` directory

## 📋 Usage

### 1. ETL Pipeline
Run the ETL process to clean and load data:
```bash
python src/etl_students.py
```

### 2. Train Machine Learning Model
Train the pass/fail prediction model:
```bash
python src/ml_predict_passfail.py
```

### 3. Generate Analysis Reports
Export data for Power BI visualization:
```bash
python src/analysis_students.py
```

### 4. Exploratory Data Analysis
Open and run the Jupyter notebook:
```bash
jupyter notebook notebooks/EDA.ipynb
```

## 🔧 Features

### Data Processing
- **Data Cleaning**: Handles missing values and data type conversions
- **Feature Engineering**: Creates pass/fail binary targets
- **Database Integration**: MySQL storage with optimized indexing

### Machine Learning
- **Random Forest Classifier**: Predicts student pass/fail outcomes
- **Feature Selection**: Uses study time, failures, absences, and grades
- **Model Persistence**: Saves trained models for future use

### Analytics & Visualization
- **Gender-based Analysis**: Pass rates by gender
- **Age-based Analysis**: Average grades by age group
- **Power BI Integration**: Interactive dashboards
- **Automated Exports**: CSV files for external analysis

## 📊 Data Sources

The project uses the **Student Performance Dataset** from UCI Machine Learning Repository, which includes:
- Student demographics (age, gender, address)
- Academic performance (grades G1, G2, G3)
- Study habits (study time, failures, absences)
- Social factors (family size, parent education)

## 🎯 Key Metrics

- **Accuracy**: Model performance on test data
- **Pass Rate**: Percentage of students passing
- **Grade Distribution**: Analysis of grade patterns
- **Demographic Insights**: Performance by gender and age

## 📈 Power BI Dashboard

The included Power BI dashboard provides:
- Interactive visualizations
- Real-time data connections
- Drill-down capabilities
- Export functionality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

This project is open source and available under the MIT License.

## 🆘 Support

For questions or issues:
1. Check the documentation
2. Review existing issues
3. Create a new issue with detailed description