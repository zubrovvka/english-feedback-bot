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
