"""
Security Utilities for English Feedback Trainer
Covers:
1. CSRF validation (Origin & Referer matching)
2. In-memory Rate Limiting per IP
3. Access Control (PIN / localhost check)
4. Input sanitization (CRLF prevention in .env)
5. Image header magic bytes validation
"""

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

_rate_limit_lock = threading.Lock()
_rate_limit_records: Dict[str, List[float]] = {}


def check_rate_limit(key: str, max_requests: int, window_seconds: int = 60) -> bool:
    """Returns True if request is allowed, False if limit exceeded."""
    now = time.time()
    with _rate_limit_lock:
        timestamps = _rate_limit_records.get(key, [])
        # Evict timestamps outside the window
        timestamps = [t for t in timestamps if now - t < window_seconds]
        if len(timestamps) >= max_requests:
            _rate_limit_records[key] = timestamps
            return False
        timestamps.append(now)
        _rate_limit_records[key] = timestamps
        return True


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
    """Checks if request is authorized by ACCESS_PIN or loopback."""
    pin = getattr(config, "ACCESS_PIN", "").strip()
    if not pin:
        return True  # No PIN configured -> open access

    # Check loopback
    remote_ip = request.remote_addr or ""
    if remote_ip in ("127.0.0.1", "::1", "localhost"):
        # Localhost is trusted by default
        return True

    # Check custom header
    req_pin = request.headers.get("X-Access-Pin", "").strip()
    if req_pin == pin:
        return True

    # Check cookie
    cookie_token = request.cookies.get("auth_pin", "").strip()
    if cookie_token == pin:
        return True

    # Check JSON body for auth endpoints
    if request.is_json and request.json:
        if request.json.get("access_pin", "").strip() == pin:
            return True

    return False
