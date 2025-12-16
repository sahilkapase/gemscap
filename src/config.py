import os

# Database Settings
# Use absolute path relative to this file's parent (src/) -> parent (root) settings
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = "market_data.db"
DB_PATH = os.path.join(BASE_DIR, DB_FILE)
DB_URL = f"sqlite:///{DB_PATH}"

# Binance WebSocket
BINANCE_WS_URL = "wss://stream.binance.com:9443/ws"

# Symbols to track
# We will track a few major pairs for analytics
SYMBOLS = [
    "btcusdt",
    "ethusdt",
    "bnbusdt",
    "solusdt",
    "adausdt"
]

# Analytics Settings
DEFAULT_TIMEFRAME = "1Min"
DEFAULT_WINDOW = 20

TIMEFRAMES = ["1s", "1Min", "5Min", "15Min", "1H"]
