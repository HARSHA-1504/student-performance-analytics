import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine

# ---------------------------
# STREAMLIT PAGE SETTINGS
# ---------------------------
st.set_page_config(page_title="🎓 Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Analytics")
st.write("This dashboard analyzes student performance data in real-time using MySQL (Railway) + Streamlit.")

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
# Replace these with your own Railway MySQL credentials
HOST = "yamanote.proxy.rlwy.net"     # Example host — replace with yours
USER = "root"
PASSWORD = "your_password_here"       # Replace with your real password
PORT = "34460"
DATABASE = "railway"

# SQLAlchemy connection string
connection_string = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create SQLAlchemy engine
engine = create_engine(connection_string)

# Load data
try:
    df = pd.read_sql("SELECT * FROM students", con=engine)
    st.success("✅ Connected to Railway MySQL Database")
except Exception as e:
    st.error(f"❌ Database connection failed: {e}")
    st.stop()

# ---------------------------
# DATA CLEANING / INSIGHTS
# ---------------------------
st.subheader("📋 Dataset Preview")
st.dataframe(df.head())

# Summary Metrics
total_students = len(df)
passed = len(df[df["final_result"] == "pass"])
failures = len(df[df["final_result"] == "fail"])
pass_rate = round((passed / total_students) * 100, 2)

# KPI cards
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Students", total_students)
col2.metric("Passed", passed)
col3.metric("Failed", failures)
col4.metric("Pass Rate (%)", f"{pass_rate}%")

# ---------------------------
# VISUALIZATIONS
# ---------------------------
st.markdown("---")

# Pass rate by gender
st.subheader("📊 Pass Rate by Gender")
gender_pass = (
    df.groupby("sex")["final_result"]
    .apply(lambda x: (x == "pass").mean() * 100)
    .reset_index()
)
st.bar_chart(gender_pass.set_index("sex"))

# Average grade by age
st.subheader("📈 Average Final Grade by Age")
if "G3" in df.columns:
    avg_grade = df.groupby("age")["G3"].mean().reset_index()
    st.line_chart(avg_grade.set_index("age"))
else:
    st.info("No 'G3' column found for grades in dataset.")

# Study time vs final grade
st.subheader("📉 Study Time vs Final Grade")
if "studytime" in df.columns and "G3" in df.columns:
    st.scatter_chart(df[["studytime", "G3"]])
else:
    st.warning("Columns 'studytime' and 'G3' not found in data.")

# ---------------------------
# RAW DATA
# ---------------------------
with st.expander("📂 View Full Dataset"):
    st.dataframe(df)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit & MySQL")
