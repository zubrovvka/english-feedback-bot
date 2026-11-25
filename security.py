"""
Security Utilities for English Feedback Trainer
Covers:
1. CSRF validation (Origin & Referer matching)
2. In-memory Rate Limiting per IP
3. Access Control (PIN / localhost check)
4. Input sanitization (CRLF prevention in .env)
5. Image header magic bytes validation
"""

import hmac
import time
import re
import threading
from urllib.parse import urlparse
from typing import Dict, List, Optional
import config

ALLOWED_VOICES = {
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-GB-SoniaNeural",
    "en-GB-RyanNeural"
}

import database

def check_rate_limit(key: str, max_requests: int, window_seconds: int = 60) -> bool:
    """Returns True if request is allowed, False if limit exceeded. Backed by SQLite."""
    return database.check_rate_limit(key, max_requests, window_seconds)


def is_safe_origin(request) -> bool:
    """Validates Origin and Referer headers against request host to prevent CSRF.
    Also checks modern browser Fetch Metadata (Sec-Fetch-Site).
    """
    # 1. Reject cross-site requests signaled by modern browsers via Fetch Metadata
    fetch_site = request.headers.get("Sec-Fetch-Site", "").strip().lower()
    if fetch_site == "cross-site":
        return False

    host = request.host.lower()

    # 2. Check Origin header if present
    origin = request.headers.get("Origin")
    if origin:
        parsed = urlparse(origin)
        if parsed.netloc.lower() != host:
            return False

    # 3. Check Referer header if present
    referer = request.headers.get("Referer")
    if referer:
        parsed = urlparse(referer)
        if parsed.netloc.lower() != host:
            return False

    return True


def sanitize_env_string(val: str, max_len: int = 128) -> str:
    """Strips newline / carriage return characters to prevent CRLF injection."""
    if not val:
        return ""
    # Remove any newline, carriage return, null bytes, or equals sign
    cleaned = re.sub(r"[\r\n\x00=]", "", val).strip()
    return cleaned[:max_len]


def is_valid_gemini_key(key: str) -> bool:
    """Validates Gemini API key format (alphanumeric, dashes, underscores)."""
    if not key:
        return True  # Empty key is allowed (to unset)
    return bool(re.match(r"^[A-Za-z0-9_-]{10,128}$", key))


def is_valid_image_bytes(data: bytes) -> bool:
    """Validates magic bytes for common web image formats (PNG, JPEG, WEBP)."""
    if not data or len(data) < 12:
        return False
    # PNG: \x89PNG\r\n\x1a\n
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return True
    # JPEG: \xff\xd8\xff
    if data.startswith(b"\xff\xd8\xff"):
        return True
    # WEBP: RIFF....WEBP
    if data.startswith(b"RIFF") and data[8:12] == b"WEBP":
        return True
    return False


def is_authorized(request) -> bool:
    """Checks if request is authorized by ACCESS_PIN or direct loopback."""
    config.reload_if_env_changed()
    pin = getattr(config, "ACCESS_PIN", "").strip()
    if not pin:
        return True  # No PIN configured -> open access

    # Check direct loopback (ignore loopback bypass if request arrived via reverse proxy)
    remote_ip = (request.remote_addr or "").strip()
    has_forwarded = bool(request.headers.get("X-Forwarded-For", "").strip())
    if not has_forwarded and remote_ip in ("127.0.0.1", "::1", "::ffff:127.0.0.1", "localhost"):
        # Direct localhost connection is trusted by default
        return True

    # Check custom header
    req_pin = (request.headers.get("X-Access-Pin") or "").strip()
    if req_pin and hmac.compare_digest(req_pin, pin):
        return True

    # Check cookie
    cookie_token = (request.cookies.get("auth_pin") or "").strip()
    if cookie_token and hmac.compare_digest(cookie_token, pin):
        return True

    # Check JSON body safely (never crash on malformed JSON or non-string field)
    json_data = request.get_json(silent=True)
    if isinstance(json_data, dict):
        body_pin = str(json_data.get("access_pin") or "").strip()
        if body_pin and hmac.compare_digest(body_pin, pin):
            return True

    return False
