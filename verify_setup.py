import sys
import os
import time
import pandas as pd

# Add current dir to path
sys.path.append(os.getcwd())

from src.config import SYMBOLS
from src.storage import db
from src.ingestion import BinanceIngestion
from src.analytics import resample_data

print("✅ Imports successful.")

# Test Storage
print("Testing Storage...")
try:
    db.store_tick("TEST", 100.0, 1.0, int(time.time()*1000))
    df = db.get_data("TEST")
    if not df.empty and df.iloc[0]['symbol'] == "TEST":
        print("✅ Storage write/read successful.")
    else:
        print("❌ Storage failed.")
except Exception as e:
    print(f"❌ Storage Error: {e}")

# Test Analytics
print("Testing Analytics...")
try:
    resampled = resample_data(df, '1Min')
    if resampled is not None:
        print("✅ Analytics resample successful.")
    else:
        print("❌ Analytics failed.")
except Exception as e:
    print(f"❌ Analytics Error: {e}")

# Test Ingestion (Short Run)
print("Testing Ingestion connection (5s)...")
try:
    ingestion = BinanceIngestion()
    ingestion.start()
    time.sleep(5)
    ingestion.stop()

    # Check if real symbols data arrived
    found_data = False
    for s in SYMBOLS:
        df = db.get_data(s.lower())
        if not df.empty:
            print(f"✅ Received data for {s}: {len(df)} ticks.")
            found_data = True
            break

    if found_data:
        print("✅ Ingestion successful.")
    else:
        print("⚠️ Ingestion ran but no data stored yet (could be connection latency).")
except Exception as e:
    print(f"❌ Ingestion Error: {e}")

print("Verification complete.")
