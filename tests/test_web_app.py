import json
import pytest
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

import app as web_app
import database as db

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "web_test.db"
    monkeypatch.setattr(db, "DB_PATH", test_db)
    db.init_db()
    web_app.app.config["TESTING"] = True
    with web_app.app.test_client() as client:
        yield client

def test_index_page(client):
    res = client.get("/")
    assert res.status_code == 200
    assert b"English Feedback" in res.data

def test_get_config(client):
    res = client.get("/api/config")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "has_gemini_key" in data
    assert "tts_voice" in data
    assert "available_voices" in data

def test_stats_and_empty_next_card(client):
    res = client.get("/api/stats")
    assert res.status_code == 200
    data = json.loads(res.data)
    assert data["total"] == 0

    res_card = client.get("/api/cards/next")
    assert res_card.status_code == 200
    card_data = json.loads(res_card.data)
    assert card_data["card"] is None

def test_review_and_list_cards(client):
    # Add sample card
    card_id = db.add_card({
        "type": "vocab",
        "front": "sample",
        "back": "образец",
        "transcription": "/ˈsɑːmpəl/",
        "example": "This is a sample."
    }, user_id=0)

    # Next card should return sample
    res_card = client.get("/api/cards/next")
    assert res_card.status_code == 200
    card_data = json.loads(res_card.data)
    assert card_data["card"]["front"] == "sample"

    # Review card
    res_rev = client.post(f"/api/cards/{card_id}/review", json={"rating": 3})
    assert res_rev.status_code == 200
    rev_data = json.loads(res_rev.data)
    assert rev_data["success"] is True

    # List cards
    res_list = client.get("/api/cards")
    assert res_list.status_code == 200
    list_data = json.loads(res_list.data)
    assert len(list_data["cards"]) == 1

    # Delete card
    res_del = client.delete(f"/api/cards/{card_id}")
    assert res_del.status_code == 200
    assert json.loads(res_del.data)["success"] is True

def test_quiz_and_cloze_and_quick_add(client):
    # Add multiple cards for quiz distractors and cloze
    c1 = db.add_card({
        "type": "vocab",
        "front": "werewolf",
        "back": "оборотень",
        "example": "He saw a fierce werewolf in the forest."
    }, user_id=0)
    c2 = db.add_card({
        "type": "vocab",
        "front": "puddle",
        "back": "лужа",
        "example": "He stepped in a muddy puddle."
    }, user_id=0)
    c3 = db.add_card({
        "type": "correction",
        "front": "discus ➔ discussion",
        "back": "discussion",
        "example": "We had an interesting discussion."
    }, user_id=0)

    # Test Quiz endpoint
    res_quiz = client.get("/api/cards/quiz")
    assert res_quiz.status_code == 200
    quiz_data = json.loads(res_quiz.data)
    assert "question" in quiz_data
    assert "correct_answer" in quiz_data
    assert len(quiz_data["options"]) >= 2

    # Test Cloze endpoint
    res_cloze = client.get("/api/cards/cloze")
    assert res_cloze.status_code == 200
    cloze_data = json.loads(res_cloze.data)
    assert "target" in cloze_data
    assert "masked_sentence" in cloze_data
    assert "__________" in cloze_data["masked_sentence"]

    # Test Quick-Add word
    res_add = client.post("/api/cards/quick-add", json={
        "word": "serendipity",
        "sentence": "It was pure serendipity.",
        "translation": "счастливая случайность"
    })
    assert res_add.status_code == 200
    add_data = json.loads(res_add.data)
    assert add_data["success"] is True
    assert add_data["card"]["front"] == "serendipity"
    assert add_data["card"]["back"] == "счастливая случайность"

def test_static_assets(client):
    res_css = client.get("/static/css/styles.css")
    assert res_css.status_code == 200
    assert b"interactive-word" in res_css.data

    res_js = client.get("/static/js/app.js")
    assert res_js.status_code == 200
    assert b"English Feedback" in res_js.data

def test_translate_endpoint(client):
    res = client.post("/api/translate", json={"text": "strangers"})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "translation" in data



