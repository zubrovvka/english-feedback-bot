import os
from pathlib import Path
from dotenv import load_dotenv

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
AUDIO_DIR = DATA_DIR / "audio"
DB_PATH = DATA_DIR / "bot_database.db"

# Load .env file
load_dotenv(BASE_DIR / ".env")

DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ACCESS_PIN = os.getenv("ACCESS_PIN", "").strip()
DEFAULT_USER_ID = 0

# Optional legacy whitelist (kept for backward compatibility with existing tests)
raw_allowed = os.getenv("ALLOWED_USER_IDS", "").strip()
ALLOWED_USER_IDS = [int(uid.strip()) for uid in raw_allowed.split(",") if uid.strip().isdigit()]

# Default Edge-TTS voice (high-quality neural English voice)
TTS_VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural").strip()
