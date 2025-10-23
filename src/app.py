import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import os

# ---------------------------
# STREAMLIT PAGE SETTINGS
# ---------------------------
st.set_page_config(page_title="🎓 Student Performance Dashboard", layout="wide")

st.title("🎓 Student Performance Analytics")
st.write("This dashboard analyzes student performance data in real-time using MySQL (Railway) + Streamlit.")

# ---------------------------
# DATABASE CONNECTION
# ---------------------------
# ✅ Securely load credentials from Streamlit Secrets
# (Add these in Streamlit Cloud > Settings > Secrets)
# HOST="your_host"
# USER="your_user"
# PASSWORD="your_password"
# PORT="your_port"
# DATABASE="your_database"

HOST = "yamanote.proxy.rlwy.net"
USER = "root"
PASSWORD = "LsMiNtwjVaLAAGqTeAPQkWviSleXbSXb"   # 🔹 Replace with real password from Railway
PORT = "34460"
DATABASE = "railway"

# SQLAlchemy connection string
connection_string = f"mysql+mysqlconnector://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}"

# Create SQLAlchemy engine
try:
    engine = create_engine(connection_string)
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
passed = len(df[df["final_result"].str.lower() == "pass"])
failures = len(df[df["final_result"].str.lower() == "fail"])
pass_rate = round((passed / total_students) * 100, 2)

# ---------------------------
# ---------------------------
# KPI SECTION (Lavender Style)
# ---------------------------
st.markdown("---")
st.markdown("### 📊 Key Performance Indicators")

# Custom CSS for Lavender Cards
st.markdown(
    """
    <style>
        .kpi-container {
            display: flex;
            justify-content: space-evenly;
            gap: 20px;
            margin-top: 20px;
        }
        .kpi-card {
            background-color: #d6c2ee; /* Lavender shade */
            border-radius: 12px;
            padding: 25px;
            flex: 1;
            text-align: center;
            color: #1a1a1a;
            box-shadow: 0 4px 10px rgba(0,0,0,0.1);
            transition: transform 0.2s ease-in-out, box-shadow 0.2s;
        }
        .kpi-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 18px rgba(0,0,0,0.15);
        }
        .kpi-title {
            font-size: 22px;
            font-weight: 600;
            color: #2b2b2b;
            margin-bottom: 10px;
        }
        .kpi-value {
            font-size: 42px;
            font-weight: bold;
            color: #000;
        }
        .kpi-sub {
            font-size: 14px;
            color: #333333;
            opacity: 0.8;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# Render KPI cards
st.markdown(
    f"""
    <div class="kpi-container">
        <div class="kpi-card">
            <div class="kpi-title">👩‍🎓 Total Students</div>
            <div class="kpi-value">{total_students}</div>
            <div class="kpi-sub">Sum of count</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">✅ Total Passed</div>
            <div class="kpi-value">{passed}</div>
            <div class="kpi-sub">Total Passed</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">❌ Failed</div>
            <div class="kpi-value">{failures}</div>
            <div class="kpi-sub">Total Failed</div>
        </div>
        <div class="kpi-card">
            <div class="kpi-title">📈 Pass Rate (%)</div>
            <div class="kpi-value">{pass_rate}%</div>
            <div class="kpi-sub">Success Percentage</div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)



# ---------------------------
# VISUALIZATIONS
# ---------------------------
st.markdown("---")

# Pass rate by gender
st.subheader("📊 Pass Rate by Gender")
if "sex" in df.columns and "final_result" in df.columns:
    gender_pass = (
        df.groupby("sex")["final_result"]
        .apply(lambda x: (x.str.lower() == "pass").mean() * 100)
        .reset_index()
    )
    st.bar_chart(gender_pass.set_index("sex"))
else:
    st.warning("⚠️ Columns 'sex' or 'final_result' missing from dataset.")

# Average grade by age
st.subheader("📈 Average Final Grade by Age")
if "G3" in df.columns and "age" in df.columns:
    avg_grade = df.groupby("age")["G3"].mean().reset_index()
    st.line_chart(avg_grade.set_index("age"))
else:
    st.info("ℹ️ No 'G3' column found for grades in dataset.")

# Study time vs final grade
st.subheader("📉 Study Time vs Final Grade")
if "studytime" in df.columns and "G3" in df.columns:
    st.scatter_chart(df[["studytime", "G3"]])
else:
    st.warning("⚠️ Columns 'studytime' or 'G3' not found in dataset.")

# ---------------------------
# RAW DATA VIEW
# ---------------------------
with st.expander("📂 View Full Dataset"):
    st.dataframe(df)

st.markdown("---")
st.caption("Built with ❤️ using Streamlit + MySQL (Railway)")
