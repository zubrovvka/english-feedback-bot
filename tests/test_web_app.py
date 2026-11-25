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
    assert b"TutorCards" in res.data

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

    # Local Tailwind bundle
    res_tailwind = client.get("/static/css/output.css")
    assert res_tailwind.status_code == 200
    assert "css" in res_tailwind.headers.get("Content-Type", "").lower()

    # Modular entry point
    res_main = client.get("/static/js/main.js")
    assert res_main.status_code == 200
    assert b"import" in res_main.data
    assert "javascript" in res_main.headers.get("Content-Type", "").lower()

    # ES modules
    for mod in ["state.js", "api.js", "ui.js", "tts.js", "srs.js", "cloze.js", "quiz.js"]:
        res_mod = client.get(f"/static/js/modules/{mod}")
        assert res_mod.status_code == 200, f"Module {mod} returned {res_mod.status_code}"
        assert "javascript" in res_mod.headers.get("Content-Type", "").lower()

    # Legacy app.js
    res_js = client.get("/static/js/app.js")
    assert res_js.status_code == 200
    assert b"English Feedback" in res_js.data

def test_translate_endpoint(client):
    res = client.post("/api/translate", json={"text": "strangers"})
    assert res.status_code == 200
    data = json.loads(res.data)
    assert "translation" in data


def test_pin_access_and_mobile_auth(client, monkeypatch):
    import config
    monkeypatch.setattr(config, "ACCESS_PIN", "4321")

    # Mobile request without auth -> 401
    res = client.get("/api/stats", environ_base={"REMOTE_ADDR": "192.168.1.100"})
    assert res.status_code == 401

    # Localhost -> allowed even with PIN configured
    res_local = client.get("/api/stats", environ_base={"REMOTE_ADDR": "127.0.0.1"})
    assert res_local.status_code == 200

    # Mobile with X-Access-Pin header -> 200
    res_header = client.get("/api/stats", environ_base={"REMOTE_ADDR": "192.168.1.100"}, headers={"X-Access-Pin": "4321"})
    assert res_header.status_code == 200

    # Mobile PIN verification -> sets cookie
    res_verify = client.post("/api/auth/verify", json={"pin": "4321"})
    assert res_verify.status_code == 200
    assert "auth_pin" in res_verify.headers.get("Set-Cookie", "")

    # Clear cookies so next checks test unauthenticated proxy/malformed requests
    client.delete_cookie("auth_pin")

    # Loopback behind reverse proxy (X-Forwarded-For) MUST require PIN
    res_proxy = client.get(
        "/api/stats",
        environ_base={"REMOTE_ADDR": "127.0.0.1"},
        headers={"X-Forwarded-For": "203.0.113.50"}
    )
    assert res_proxy.status_code == 401

    # Malformed JSON with PIN active must fail cleanly with 401 (no 500 AttributeError)
    res_bad_json = client.post(
        "/api/cards/quick-add",
        data="{not-json",
        content_type="application/json",
        environ_base={"REMOTE_ADDR": "192.168.1.100"}
    )
    assert res_bad_json.status_code == 401


def test_config_pin_preservation_and_env_reload(client, tmp_path, monkeypatch):
    import config
    env_file = tmp_path / ".env"
    env_file.write_text("ACCESS_PIN=2882\nTTS_VOICE=en-US-JennyNeural\n", encoding="utf-8")
    monkeypatch.setattr(config, "ENV_PATH", env_file)
    monkeypatch.setattr(config, "_last_env_mtime_ns", None)
    monkeypatch.setattr(config, "ACCESS_PIN", "2882")
    monkeypatch.setattr(config, "TTS_VOICE", "en-US-JennyNeural")
    config.sync_env_mtime()

    # 1. Saving TTS voice with empty/missing access_pin MUST preserve ACCESS_PIN
    res = client.post(
        "/api/config",
        json={"tts_voice": "en-GB-SoniaNeural", "access_pin": ""},
        environ_base={"REMOTE_ADDR": "192.168.1.100"},
        headers={"X-Access-Pin": "2882"}
    )
    assert res.status_code == 200
    data = res.get_json()
    assert data["has_pin"] is True
    assert config.ACCESS_PIN == "2882"
    assert config.TTS_VOICE == "en-GB-SoniaNeural"

    # 2. Updating PIN updates config + Set-Cookie
    res2 = client.post(
        "/api/config",
        json={"access_pin": "9876"},
        environ_base={"REMOTE_ADDR": "192.168.1.100"},
        headers={"X-Access-Pin": "2882"}
    )
    assert res2.status_code == 200
    assert config.ACCESS_PIN == "9876"
    assert "auth_pin=9876" in res2.headers.get("Set-Cookie", "")

    # 3. External .env edit (simulating another WSGI worker) is picked up automatically
    import time
    time.sleep(0.02)
    env_file.write_text("ACCESS_PIN=5555\nTTS_VOICE=en-GB-RyanNeural\n", encoding="utf-8")
    res_old = client.get("/api/stats", environ_base={"REMOTE_ADDR": "192.168.1.100"}, headers={"X-Access-Pin": "9876"})
    assert res_old.status_code == 401
    res_new = client.get("/api/stats", environ_base={"REMOTE_ADDR": "192.168.1.100"}, headers={"X-Access-Pin": "5555"})
    assert res_new.status_code == 200

    # 4. Explicit clear_pin disables PIN protection
    res3 = client.post(
        "/api/config",
        json={"clear_pin": True},
        environ_base={"REMOTE_ADDR": "192.168.1.100"},
        headers={"X-Access-Pin": "5555"}
    )
    assert res3.status_code == 200
    assert res3.get_json()["has_pin"] is False
    assert config.ACCESS_PIN == ""


def test_tts_card_endpoint_regex_and_dynamic_voice(client, tmp_path, monkeypatch):
    import config
    import tts_service
    monkeypatch.setattr(config, "AUDIO_DIR", tmp_path)

    cid = db.add_card({
        "type": "correction",
        "front": "Как сказать правильно: she go?",
        "back": "she goes",
        "pronunciation_text": "❌ she go ➔ ✅ she goes"
    }, user_id=0)

    called_voices = []
    async def fake_generate(text, filename_prefix="card"):
        called_voices.append((text, config.TTS_VOICE))
        p = tmp_path / f"{filename_prefix}_{config.TTS_VOICE}.mp3"
        p.write_bytes(b"ID3test")
        return p

    monkeypatch.setattr(tts_service, "generate_speech", fake_generate)
    res = client.get(f"/api/tts/{cid}")
    assert res.status_code == 200
    assert called_voices[0][0] == "she go she goes"


def test_quiz_distractors_are_unique(test_db):
    from services import quiz_service
    # Add 4 cards where 2 have identical 'back' values
    db.add_card({"type": "vocab", "front": "a1", "back": "same_meaning"}, user_id=0)
    db.add_card({"type": "vocab", "front": "a2", "back": "same_meaning"}, user_id=0)
    db.add_card({"type": "vocab", "front": "a3", "back": "other_1"}, user_id=0)
    db.add_card({"type": "vocab", "front": "a4", "back": "other_2"}, user_id=0)

    for _ in range(10):
        q = quiz_service.build_quiz_question(user_id=0)
        assert q is not None
        assert len(q["options"]) == len(set(q["options"]))





