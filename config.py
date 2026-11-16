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
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

# Whitelist: List of allowed Telegram User IDs (comma-separated, e.g. "12345678,98765432")
# If empty, a warning is shown, and the bot informs the first user who types /start what their ID is.
raw_allowed = os.getenv("ALLOWED_USER_IDS", "").strip()
ALLOWED_USER_IDS = [int(uid.strip()) for uid in raw_allowed.split(",") if uid.strip().isdigit()]

# Default Edge-TTS voice (high-quality neural English voice)
TTS_VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural").strip()
