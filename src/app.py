from flask import Flask
import threading
import time
import subprocess

app = Flask(__name__)

# Run your ETL + Analysis in background
def run_analytics():
    try:
        print("🚀 Starting ETL process...")
        subprocess.run(["python", "src/etl_students.py"], check=True)
        print("✅ ETL process completed.")
        
        print("📊 Starting Analysis process...")
        subprocess.run(["python", "src/analysis_students.py"], check=True)
        print("✅ Analysis completed successfully.")
    except Exception as e:
        print(f"⚠️ Error during background process: {e}")

# Run scripts only once when the app starts
threading.Thread(target=run_analytics, daemon=True).start()

@app.route("/")
def home():
    return "🎯 Student Performance Analytics is running successfully on Render!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

