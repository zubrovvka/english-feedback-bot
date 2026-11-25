import os
import threading
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv, dotenv_values

# Paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
AUDIO_DIR = DATA_DIR / "audio"
DB_PATH = DATA_DIR / "bot_database.db"
ENV_PATH = BASE_DIR / ".env"

DATA_DIR.mkdir(parents=True, exist_ok=True)
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

_env_lock = threading.Lock()


def _get_env_mtime_ns() -> Optional[int]:
    try:
        return ENV_PATH.stat().st_mtime_ns
    except OSError:
        return None


# Load .env file on initial import
load_dotenv(ENV_PATH)
_last_env_mtime_ns: Optional[int] = _get_env_mtime_ns()

# Environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ACCESS_PIN = os.getenv("ACCESS_PIN", "").strip()
DEFAULT_USER_ID = 0

# Optional legacy whitelist (kept for backward compatibility with existing tests)
raw_allowed = os.getenv("ALLOWED_USER_IDS", "").strip()
ALLOWED_USER_IDS = [int(uid.strip()) for uid in raw_allowed.split(",") if uid.strip().isdigit()]

# Default Edge-TTS voice (high-quality neural English voice)
TTS_VOICE = os.getenv("TTS_VOICE", "en-US-JennyNeural").strip()


def reload_if_env_changed() -> None:
    """Reloads dynamic settings if .env changed on disk (keeps multi-worker WSGI processes in sync)."""
    global GEMINI_API_KEY, ACCESS_PIN, TTS_VOICE, _last_env_mtime_ns
    current_mtime = _get_env_mtime_ns()
    if current_mtime == _last_env_mtime_ns:
        return

    with _env_lock:
        current_mtime = _get_env_mtime_ns()
        if current_mtime == _last_env_mtime_ns:
            return
        values = dotenv_values(ENV_PATH) if current_mtime is not None else {}
        if "GEMINI_API_KEY" in values:
            GEMINI_API_KEY = (values.get("GEMINI_API_KEY") or "").strip()
        if "ACCESS_PIN" in values:
            ACCESS_PIN = (values.get("ACCESS_PIN") or "").strip()
        if "TTS_VOICE" in values:
            TTS_VOICE = (values.get("TTS_VOICE") or "en-US-JennyNeural").strip()
        _last_env_mtime_ns = current_mtime


def sync_env_mtime() -> None:
    """Records current .env mtime after in-process write so redundant reload is skipped."""
    global _last_env_mtime_ns
    _last_env_mtime_ns = _get_env_mtime_ns()
