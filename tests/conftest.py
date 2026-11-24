"""
Shared Pytest Fixtures and Test Configuration
"""

import os
import sys
from pathlib import Path
import pytest

# Ensure project root is first in python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import database as db
import config


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    """Provides an isolated temporary SQLite database for tests."""
    db_file = tmp_path / "test_trainer.db"
    monkeypatch.setattr(db, "DB_PATH", db_file)
    db.init_db()
    return db_file


@pytest.fixture
def client(test_db):
    """Provides a configured Flask test client."""
    import app as web_app
    web_app.app.config["TESTING"] = True
    with web_app.app.test_client() as c:
        yield c


@pytest.fixture
def sample_cards(test_db):
    """Seeds a representative collection of cards for active recall and quiz testing."""
    c1 = db.add_card({
        "type": "vocab",
        "front": "serendipity",
        "back": "счастливая случайность",
        "transcription": "/ˌser.ənˈdɪp.ə.ti/",
        "example": "Finding this book was pure serendipity.",
        "pronunciation_text": "serendipity"
    }, user_id=0)

    c2 = db.add_card({
        "type": "vocab",
        "front": "ephemeral",
        "back": "эфемерный, недолговечный",
        "transcription": "/ɪˈfem.ər.əl/",
        "example": "Fashion trends are ephemeral.",
        "pronunciation_text": "ephemeral"
    }, user_id=0)

    c3 = db.add_card({
        "type": "correction",
        "front": "Как сказать правильно: I have a mistake?",
        "back": "I made a mistake",
        "explanation": "С ошибками используется глагол make",
        "example": "❌ I have a mistake ➔ ✅ I made a mistake",
        "pronunciation_text": "I made a mistake"
    }, user_id=0)

    c4 = db.add_card({
        "type": "good_language",
        "front": "Вспомни выражение: «начать с чистого листа»",
        "back": "start with a clean slate",
        "explanation": "начать с чистого листа",
        "example": "Let's start with a clean slate this quarter.",
        "pronunciation_text": "start with a clean slate"
    }, user_id=0)

    c5 = db.add_card({
        "type": "suggestion",
        "front": "Как сказать более продвинуто вместо: «very good»?",
        "back": "superb, outstanding",
        "explanation": "Используйте сильные прилагательные",
        "example": "Вместо «very good» лучше: superb, outstanding",
        "pronunciation_text": "superb"
    }, user_id=0)

    c6 = db.add_card({
        "type": "antonym",
        "front": "diligent ↔ lazy",
        "back": "прилежный ↔ ленивый",
        "transcription": "/ˈdɪl.ɪ.dʒənt/",
        "example": "diligent ↔ lazy (прилежный ↔ ленивый)",
        "pronunciation_text": "diligent"
    }, user_id=0)

    return {
        "vocab_1": c1,
        "vocab_2": c2,
        "correction": c3,
        "good_language": c4,
        "suggestion": c5,
        "antonym": c6
    }
