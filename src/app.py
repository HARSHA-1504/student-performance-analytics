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
# KPI SECTION (Styled)
# ---------------------------
st.markdown("---")
st.markdown("### 📊 Key Performance Indicators")

# Custom CSS for styling KPI boxes
st.markdown(
    """
    <style>
        .metric-container {
            display: flex;
            justify-content: space-around;
            background-color: #f7f9fb;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
            margin-bottom: 25px;
        }
        .metric-box {
            flex: 1;
            text-align: center;
            background: white;
            padding: 20px;
            margin: 0 10px;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: transform 0.2s ease-in-out;
        }
        .metric-box:hover {
            transform: translateY(-5px);
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
        }
        .metric-title {
            font-size: 18px;
            color: #333;
            font-weight: 600;
            margin-bottom: 8px;
        }
        .metric-value {
            font-size: 36px;
            color: #0078ff;
            font-weight: bold;
        }
        .pass { color: #16a34a; }
        .fail { color: #dc2626; }
        .rate { color: #9333ea; }
    </style>
    """,
    unsafe_allow_html=True
)

# Display KPI cards
st.markdown(
    f"""
    <div class="metric-container">
        <div class="metric-box">
            <div class="metric-title">👩‍🎓 Total Students</div>
            <div class="metric-value">{total_students}</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">✅ Passed</div>
            <div class="metric-value pass">{passed}</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">❌ Failed</div>
            <div class="metric-value fail">{failures}</div>
        </div>
        <div class="metric-box">
            <div class="metric-title">📈 Pass Rate (%)</div>
            <div class="metric-value rate">{pass_rate}%</div>
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
