import sys
import os
import time
import pandas as pd
from sqlalchemy import create_engine, text
from datetime import datetime, timedelta

# Add src to path
sys.path.append(os.path.join(os.getcwd(), "src"))
from config import DB_URL

def check_status():
    print("--- System Diagnostic ---")
    
    # 1. Check Database connection
    try:
        engine = create_engine(DB_URL)
        with engine.connect() as conn:
            # Check row count
            result = conn.execute(text("SELECT COUNT(*) FROM ticks")).scalar()
            print(f"✅ Database connected. Total Ticks: {result}")
            
            # Check recency
            last_time = conn.execute(text("SELECT MAX(timestamp) FROM ticks")).scalar()
            if last_time:
                last_time = pd.to_datetime(last_time)
                now = datetime.now()
                diff = (now - last_time).total_seconds()
                
                print(f"🕒 Last Tick Time: {last_time} (approx {diff:.1f}s ago)")
                
                if diff < 15:
                    print("✅ Data Ingestion is ACTIVE and LIVE.")
                else:
                    print("⚠️ Data Ingestion seems STALLED (no data in last 15s).")
            else:
                print("⚠️ Database is empty.")
                
            # Check Symbols
            symbols = conn.execute(text("SELECT DISTINCT symbol FROM ticks")).fetchall()
            sym_list = [r[0] for r in symbols]
            print(f"📈 Tracking Symbols: {sym_list}")
            
    except Exception as e:
        print(f"❌ Database Error: {e}")
        print("Note: If the app is running multiple instances, the DB might be locked.")

if __name__ == "__main__":
    check_status()
