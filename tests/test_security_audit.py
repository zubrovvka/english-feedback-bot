"""
Security Audit Tests: Hardening, CSRF, Magic-Bytes, CRLF, Path Traversal, and HTTPS Cookies
"""

import io
import pytest
import config
import database as db
import tts_service


class TestTtsServiceHardening:
    """Verifies that TTS generation is immune to path traversal and empty input."""

    @pytest.mark.asyncio
    async def test_empty_string_rejected(self):
        with pytest.raises(ValueError, match="cannot be empty"):
            await tts_service.generate_speech("   ")

    @pytest.mark.asyncio
    async def test_path_traversal_blocked(self):
        out_path = await tts_service.generate_speech("test text", filename_prefix="../../malicious")
        # Ensure file was created strictly inside AUDIO_DIR, not in parent directories
        assert config.AUDIO_DIR.resolve() in out_path.resolve().parents


class TestWebSecurityHardening:
    """Verifies HTTP security headers, CSRF protection, input validation and cookie attributes."""

    def test_security_headers_present(self, client):
        res = client.get("/")
        assert res.status_code == 200
        assert res.headers.get("X-Content-Type-Options") == "nosniff"
        assert res.headers.get("X-Frame-Options") == "DENY"
        assert "default-src" in res.headers.get("Content-Security-Policy", "")
        assert res.headers.get("Referrer-Policy") == "strict-origin-when-cross-origin"

    def test_csrf_untrusted_origin_blocked(self, client):
        import app as web_app
        web_app.app.config["TESTING"] = False  # Enable production CSRF checks
        try:
            res = client.post(
                "/api/cards/quick-add",
                json={"word": "test"},
                headers={"Origin": "https://evil-attacker.com"}
            )
            assert res.status_code == 403
            assert b"CSRF" in res.data or b"Forbidden" in res.data
        finally:
            web_app.app.config["TESTING"] = True

    def test_csrf_sec_fetch_site_cross_site_blocked(self, client):
        import app as web_app
        web_app.app.config["TESTING"] = False
        try:
            res = client.post(
                "/api/cards/quick-add",
                json={"word": "test"},
                headers={"Sec-Fetch-Site": "cross-site"}
            )
            assert res.status_code == 403
        finally:
            web_app.app.config["TESTING"] = True

    def test_crlf_and_invalid_gemini_key_rejected(self, client):
        # Key containing newline / CRLF injection attempt
        res = client.post("/api/config", json={"gemini_api_key": "AIzaSyTest\nATTACKER_ENV=1"})
        assert res.status_code == 400
        assert b"\xd0\x9d\xd0\xb5\xd0\xba\xd0\xbe\xd1\x80\xd1\x80\xd0\xb5\xd0\xba\xd1\x82\xd0\xbd\xd1\x8b\xd0\xb9" in res.data or b"Gemini" in res.data

    def test_invalid_tts_voice_rejected(self, client):
        # Disallowed voice names or shell injection attempts
        res = client.post("/api/config", json={"tts_voice": "malicious-voice; rm -rf /"})
        assert res.status_code == 400

    def test_upload_invalid_magic_bytes_rejected(self, client):
        # Fake png file containing shell script bytes
        fake_file = io.BytesIO(b"#!/bin/bash\necho hacked")
        res = client.post(
            "/api/upload",
            data={"file": (fake_file, "script.png")}
        )
        assert res.status_code == 400
        json_data = res.get_json()
        assert "error" in json_data
        assert "Недопустимый" in json_data["error"] or "формат" in json_data["error"].lower()

    def test_cookie_secure_flag_on_https(self, client, monkeypatch):
        monkeypatch.setattr(config, "ACCESS_PIN", "9999")
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

    @pytest.mark.parametrize("bad_pin", ["", "   ", "wrong_pin", "0000", "12345678901234567890"])
    def test_invalid_pin_rejected(self, client, monkeypatch, bad_pin):
        monkeypatch.setattr(config, "ACCESS_PIN", "4321")
        res = client.post("/api/auth/verify", json={"pin": bad_pin})
        assert res.status_code == 401
        data = res.get_json()
        assert data.get("success") is not True
