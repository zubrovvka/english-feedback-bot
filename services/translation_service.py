"""
Translation Service
Translates English words, phrases, and sentences to Russian.
Uses Gemini API if key is set, with automatic fallback to Google Translate.
"""

import json
import logging
import re
import urllib.parse
from typing import Dict, Any, Optional
import httpx
import config
import database as db

logger = logging.getLogger(__name__)


def clean_text_for_translation(text: str) -> str:
    """Removes emoji, prefixes, and markdown from text before translating."""
    if not text:
        return ""
    # Remove markers like '❌ she never talk ➔ ✅'
    text = re.sub(r"[❌✅➔💡⭐🔤—–\-–>]", " ", text)
    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text).strip()
    return text


def translate_with_google(text: str) -> str:
    """Translates text from English to Russian using Google's dictionary/translate API."""
    clean = clean_text_for_translation(text)
    if not clean:
        return ""

    url = "https://clients5.google.com/translate_a/t"
    params = {
        "client": "dict-chrome-ex",
        "sl": "en",
        "tl": "ru",
        "q": clean
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    try:
        resp = httpx.get(url, params=params, headers=headers, timeout=6.0)
        if resp.status_code == 200:
            data = resp.json()
            if isinstance(data, list) and len(data) > 0:
                result = data[0]
                if isinstance(result, str):
                    return result.strip()
                elif isinstance(result, list) and len(result) > 0:
                    return str(result[0]).strip()
    except Exception as e:
        logger.warning(f"Google translate API error for '{clean[:30]}': {e}")

    # Fallback to MyMemory if Google fails
    try:
        mm_url = "https://api.mymemory.translated.net/get"
        mm_resp = httpx.get(mm_url, params={"q": clean, "langpair": "en|ru"}, timeout=5.0)
        if mm_resp.status_code == 200:
            mm_data = mm_resp.json()
            translated = mm_data.get("responseData", {}).get("translatedText")
            if translated and translated.lower() != clean.lower():
                return translated.strip()
    except Exception as e:
        logger.warning(f"MyMemory translate fallback error: {e}")

    return ""


def translate_text(text: str) -> str:
    """Main translation entrypoint."""
    if not text or not text.strip():
        return ""
    return translate_with_google(text)


def get_or_create_card_translation(card: Dict[str, Any]) -> str:
    """Returns stored translation or generates, saves, and returns it."""
    card_id = card.get("id")
    existing = card.get("translation")
    if existing and existing.strip():
        return existing.strip()

    # Determine what text to translate based on card type
    card_type = card.get("type", "vocab")
    back = card.get("back", "").strip()
    front = card.get("front", "").strip()

    target_text = ""
    if card_type in ("correction", "corrections", "good_language", "suggestion", "suggestions"):
        # The back is the English corrected sentence / phrase
        target_text = back
    elif card_type == "vocab":
        # If back is Russian or definition, front is English word
        # If back is English definition, translate front or back
        target_text = front if not re.search(r"[а-яА-Я]", front) else back

    if not target_text:
        target_text = back or front

    # Don't translate if already primarily in Russian
    cyrillic_chars = len(re.findall(r"[а-яА-ЯёЁ]", target_text))
    latin_chars = len(re.findall(r"[a-zA-Z]", target_text))
    if cyrillic_chars > latin_chars:
        return ""

    translation = translate_text(target_text)
    if translation and card_id:
        try:
            conn = db.get_connection()
            cur = conn.cursor()
            cur.execute("UPDATE cards SET translation = ? WHERE id = ?", (translation, card_id))
            conn.commit()
            conn.close()
        except Exception as e:
            logger.error(f"Failed to save translation for card {card_id}: {e}")

    return translation
