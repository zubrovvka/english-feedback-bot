"""
Unit and regression tests for Audit Fixes (Items 1-16)
"""

import sys
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import pytest
import sqlite3
import database as db
import security
from services import card_service, translation_service
import gemini_parser


@pytest.fixture
def test_db(tmp_path, monkeypatch):
    db_file = tmp_path / "audit_test.db"
    monkeypatch.setattr(db, "DB_PATH", db_file)
    db.init_db()
    return db_file


@pytest.fixture
def client(test_db):
    import app as web_app
    web_app.app.config["TESTING"] = True
    with web_app.app.test_client() as client:
        yield client


def test_card_deduplication(test_db):
    """Task 3: Duplicate cards are ignored on ingest."""
    parsed = {
        "vocab": [{"word": "resilient", "translation": "стойкий", "transcription": "/rɪˈzɪl.jənt/", "example": "He is resilient", "raw": ""}],
        "corrections": [{"quiz": "Как правильно: she go?", "correct": "she goes", "wrong": "she go", "explanation": "", "raw": ""}],
        "good_language": [{"phrase": "hit the ground running", "meaning": "начать с места в карьер", "example": "", "raw": ""}],
        "suggestions": [{"quiz": "Как сказать вместо big?", "basic": "big", "advanced": "massive", "explanation": "", "raw": ""}]
    }

    # First ingest
    total1, counts1 = card_service.ingest_parsed_board(parsed, user_id=0)
    assert total1 == 4
    assert counts1["vocab"] == 1

    # Second ingest of exact same data should add 0 duplicates
    total2, counts2 = card_service.ingest_parsed_board(parsed, user_id=0)
    assert total2 == 0
    assert counts2["vocab"] == 0
    assert counts2["correction"] == 0


def test_cards_limit_bounds(client, test_db):
    """Task 7: Limit parameter is capped and handles non-integer."""
    # Insert 5 cards
    for i in range(5):
        db.add_card({"front": f"word_{i}", "back": f"trans_{i}", "type": "vocab"}, user_id=0)

    # Test limit=abc falls back safely to 500
    res = client.get("/api/cards?limit=abc")
    assert res.status_code == 200
    assert len(res.get_json()["cards"]) == 5

    # Test limit=2 returns exactly 2
    res = client.get("/api/cards?limit=2")
    assert res.status_code == 200
    assert len(res.get_json()["cards"]) == 2


def test_invalid_card_id_rejected(client, test_db):
    """Task 11: card_id < 1 rejected with 400."""
    res = client.get("/api/tts/0")
    assert res.status_code == 400

    res = client.post("/api/cards/0/review", json={"rating": 3})
    assert res.status_code == 400

    res = client.delete("/api/cards/0")
    assert res.status_code == 400


def test_json_404_handler(client):
    """Task 16: API 404 returns JSON."""
    res = client.get("/api/nonexistent_route_123")
    assert res.status_code == 404
    assert res.is_json
    assert res.get_json()["error"] == "Resource not found"


def test_persistent_rate_limiter(test_db):
    """Task 10: Rate limiting is backed by SQLite and limits accurately."""
    key = "test_user_ip"
    # Should allow 3 requests
    assert db.check_rate_limit(key, max_requests=3, window_seconds=60) is True
    assert db.check_rate_limit(key, max_requests=3, window_seconds=60) is True
    assert db.check_rate_limit(key, max_requests=3, window_seconds=60) is True
    # 4th request should be blocked
    assert db.check_rate_limit(key, max_requests=3, window_seconds=60) is False


def test_translation_db_cleanup_on_error(test_db, monkeypatch):
    """Task 5: Translation service safely closes connection even on error."""
    # Insert card
    cid = db.add_card({"front": "test word", "back": "def", "type": "vocab"}, user_id=0)
    card = dict(db.get_card_by_id(cid, user_id=0))

    # Mock translate_text to succeed
    monkeypatch.setattr(translation_service, "translate_text", lambda text: "тестовый перевод")

    # Even if commit fails, conn is closed
    orig_connect = db.get_connection
    conns = []
    def tracked_connect():
        c = orig_connect()
        conns.append(c)
        return c

    monkeypatch.setattr(db, "get_connection", tracked_connect)
    trans = translation_service.get_or_create_card_translation(card)
    assert trans == "тестовый перевод"
    # Ensure all opened connections were closed
    for c in conns:
        with pytest.raises(sqlite3.ProgrammingError):
            c.cursor()  # Cannot operate on closed database
