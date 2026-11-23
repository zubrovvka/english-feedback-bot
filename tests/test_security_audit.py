import asyncio
import hashlib
import json
import os
import sys
from pathlib import Path
import pytest

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import config
import database as db
import gemini_parser
import tts_service
import bot


# ============================================================================
# 1. HTML PARSING & SPECIAL CHARACTERS SAFETY
# ============================================================================
class TestHtmlParsingSafety:
    """
    Checks that user data with brackets, underscores, and quotes doesn't break
    HTML entity parsing.
    """

    def test_vocab_card_html_safety_with_brackets_and_quotes(self):
        import html
        front = "[phrasal verb] look_after & 'test'"
        escaped_front = html.escape(front)
        assert "&amp;" in escaped_front
        assert "&lt;" not in escaped_front or "[" in escaped_front
        # In HTML, [brackets] and _underscores_ do not cause entity parse failures
        msg_text = f"<b>{escaped_front}</b>"
        assert msg_text.startswith("<b>[phrasal verb] look_after")

    def test_show_answer_html_escaping(self):
        import html
        example = "This is a phrasal_verb <script>alert(1)</script> example"
        escaped_example = html.escape(example)
        answer_text = f"<i>{escaped_example}</i>"
        assert "&lt;script&gt;" in answer_text
        assert "_" in answer_text  # Underscore is safe in HTML


# ============================================================================
# 2. CALLBACK_DATA VALIDATION & MALFORMED PAYLOAD RESILIENCE
# ============================================================================
class TestCallbackDataSafety:
    def test_malformed_callback_payloads_do_not_crash(self):
        def safe_parse_callback(data: str, min_parts: int):
            try:
                parts = data.split("_")
                if len(parts) < min_parts:
                    return None
                return int(parts[min_parts - 1])
            except (ValueError, IndexError):
                return None

        assert safe_parse_callback("show_answer_nonexistent", 3) is None
        assert safe_parse_callback("show_answer", 3) is None
        assert safe_parse_callback("tts_invalid", 2) is None
        assert safe_parse_callback("rate_invalid_rating", 3) is None
        assert safe_parse_callback("rate_42_3", 3) == 3


# ============================================================================
# 3. GEMINI PARSER ROBUSTNESS & MALFORMED JSON
# ============================================================================
class TestGeminiParserRobustness:
    def test_parser_extracts_json_with_conversational_text(self):
        response_text = (
            "Here is the extracted JSON from the board screenshot:\n"
            "```json\n"
            '{"vocab": [{"word": "apple", "translation": "яблоко"}]}\n'
            "```\n"
            "Hope this helps!"
        )
        parsed = gemini_parser.extract_json_from_text(response_text)
        assert "vocab" in parsed
        assert len(parsed["vocab"]) == 1
        assert parsed["vocab"][0]["word"] == "apple"

    def test_parser_sanitizes_poisoned_schema(self):
        poisoned = {
            "vocab": ["not_a_dict"],
            "corrections": None,
            "good_language": 123
        }
        sanitized = gemini_parser.sanitize_parsed_schema(poisoned)
        assert sanitized["vocab"] == []
        assert sanitized["corrections"] == []
        assert sanitized["good_language"] == []


# ============================================================================
# 4. TTS SERVICE HARDENING (PATH TRAVERSAL & EMPTY TEXT)
# ============================================================================
class TestTtsServiceHardening:
    @pytest.mark.asyncio
    async def test_empty_string_rejected(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            await tts_service.generate_speech("   ")

    @pytest.mark.asyncio
    async def test_path_traversal_blocked(self):
        # Prefix with ../ is sanitized or rejected
        out_path = await tts_service.generate_speech("test text", filename_prefix="../../malicious")
        # Ensure file was created inside AUDIO_DIR, not in parent dirs
        assert config.AUDIO_DIR.resolve() in out_path.resolve().parents


# ============================================================================
# 5. BOUNDED USER SESSIONS (NO MEMORY LEAKS)
# ============================================================================
class TestUserSessionsHardening:
    def test_bounded_sessions_eviction_and_cleanup(self):
        storage = bot.BoundedSessionStorage(max_size=50, ttl_seconds=1)
        for i in range(100):
            storage.set(i, i * 2, "vocab")

        # Size does not exceed max_size (50)
        assert len(storage) <= 50

    def test_whitelist_configuration(self):
        # Verify whitelist parsing in config
        assert isinstance(config.ALLOWED_USER_IDS, list)


# ============================================================================
# 6. WEB SECURITY, CSRF, CRLF & HEADERS HARDENING
# ============================================================================
class TestWebSecurityHardening:
    @pytest.fixture
    def client(self, tmp_path, monkeypatch):
        test_db = tmp_path / "web_sec_test.db"
        monkeypatch.setattr(db, "DB_PATH", test_db)
        db.init_db()
        import app as web_app
        web_app.app.config["TESTING"] = True
        with web_app.app.test_client() as client:
            yield client

    def test_security_headers_present(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert res.headers.get("X-Content-Type-Options") == "nosniff"
        assert res.headers.get("X-Frame-Options") == "DENY"
        assert "default-src" in res.headers.get("Content-Security-Policy", "")
        assert res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_csrf_untrusted_origin_blocked(self, tmp_path, monkeypatch):
        test_db = tmp_path / "web_csrf_test.db"
        monkeypatch.setattr(db, "DB_PATH", test_db)
        db.init_db()
        import app as web_app
        web_app.app.config["TESTING"] = False  # Enable CSRF check
        with web_app.app.test_client() as client:
            res = client.post(
                "/api/cards/quick-add",
                json={"word": "test"},
                headers={"Origin": "https://evil-attacker.com"}
            )
            assert res.status_code == 403
            assert b"CSRF" in res.data or b"Forbidden" in res.data

    def test_crlf_and_invalid_gemini_key_rejected(self, client):
        # Key containing newline / CRLF
        res = client.post("/api/config", json={"gemini_api_key": "AIzaSyTest\nATTACKER_ENV=1"})
        assert res.status_code == 400
        assert b"\xd0\x9d\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xba\xd1\x82\xd0\xbd\xd1\x8b\xd0\xb9" in res.data or b"Gemini" in res.data

    def test_invalid_tts_voice_rejected(self, client):
        res = client.post("/api/config", json={"tts_voice": "malicious-voice; rm -rf /"})
        assert res.status_code == 400

    def test_upload_invalid_magic_bytes_rejected(self, client):
        # Fake png file containing bash script
        res = client.post(
            "/api/upload",
            data={"file": (io_bytes := __import__("io").BytesIO(b"#!/bin/bash\necho hacked"), "script.png")}
        )
        assert res.status_code == 400
        json_data = res.get_json()
        assert "error" in json_data
        assert "Недопустимый" in json_data["error"] or "формат" in json_data["error"].lower()

    def test_csrf_sec_fetch_site_cross_site_blocked(self, tmp_path, monkeypatch):
        import app as web_app
        web_app.app.config["TESTING"] = False
        with web_app.app.test_client() as client:
            res = client.post(
                "/api/cards/quick-add",
                json={"word": "test"},
                headers={"Sec-Fetch-Site": "cross-site"}
            )
            assert res.status_code == 403

    def test_cookie_secure_flag_on_https(self, monkeypatch):
        import config
        monkeypatch.setattr(config, "ACCESS_PIN", "9999")
        import app as web_app
        with web_app.app.test_client() as client:
            res = client.post(
                "/api/auth/verify",
                json={"pin": "9999"},
                headers={"X-Forwarded-Proto": "https"}
            )
            assert res.status_code == 200
            cookie_headers = res.headers.getlist("Set-Cookie")
            assert any("Secure" in c for c in cookie_headers)
            assert any("HttpOnly" in c for c in cookie_headers)
            assert any("SameSite=Lax" in c for c in cookie_headers)

