"""
Card Service
Handles:
1. Converting parsed board sections (vocab, corrections, good language, suggestions) into cards.
2. Quick-add card formatting with auto-translation and context enrichment.
"""

import re
from typing import Dict, Any, Tuple
import database as db


def ingest_parsed_board(parsed_data: Dict[str, Any], user_id: int = 0) -> Tuple[int, Dict[str, int]]:
    """Saves items extracted from a Miro board into the database."""
    vocab_items = parsed_data.get("vocab", [])
    corrections = parsed_data.get("corrections", [])
    good_lang = parsed_data.get("good_language", [])
    suggestions = parsed_data.get("suggestions", [])

    added_counts = {"vocab": 0, "correction": 0, "good_language": 0, "suggestion": 0}

    for item in vocab_items:
        front = item.get("word", "").strip()
        if not front or db.card_exists(front, "vocab", user_id=user_id):
            continue
        db.add_card({
            "type": "vocab",
            "front": front,
            "back": item.get("translation", ""),
            "transcription": item.get("transcription", ""),
            "example": item.get("example", ""),
            "pronunciation_text": front,
            "raw_original": item.get("raw", "")
        }, user_id=user_id)
        added_counts["vocab"] += 1

    for item in corrections:
        front = item.get("quiz", f"Как сказать правильно: {item.get('wrong')}?").strip()
        if not front or db.card_exists(front, "correction", user_id=user_id):
            continue
        db.add_card({
            "type": "correction",
            "front": front,
            "back": item.get("correct", ""),
            "explanation": item.get("explanation", ""),
            "example": f"❌ {item.get('wrong')} ➔ ✅ {item.get('correct')}",
            "pronunciation_text": item.get("correct", ""),
            "raw_original": item.get("raw", "")
        }, user_id=user_id)
        added_counts["correction"] += 1

    for item in good_lang:
        front = f"Вспомни выражение: «{item.get('meaning', item.get('phrase'))}»".strip()
        if not front or db.card_exists(front, "good_language", user_id=user_id):
            continue
        db.add_card({
            "type": "good_language",
            "front": front,
            "back": item.get("phrase", ""),
            "explanation": item.get("meaning", ""),
            "example": item.get("example", ""),
            "pronunciation_text": item.get("phrase", ""),
            "raw_original": item.get("raw", "")
        }, user_id=user_id)
        added_counts["good_language"] += 1

    for item in suggestions:
        front = item.get("quiz", f"Как сказать более продвинуто вместо: «{item.get('basic')}»?").strip()
        if not front or db.card_exists(front, "suggestion", user_id=user_id):
            continue
        db.add_card({
            "type": "suggestion",
            "front": front,
            "back": item.get("advanced", ""),
            "explanation": item.get("explanation", ""),
            "example": f"Вместо «{item.get('basic')}» лучше: {item.get('advanced')}",
            "pronunciation_text": item.get("advanced", ""),
            "raw_original": item.get("raw", "")
        }, user_id=user_id)
        added_counts["suggestion"] += 1

    total = sum(added_counts.values())
    return total, added_counts


def create_quick_add_card(
    word: str,
    translation: str = "",
    sentence: str = "",
    transcription: str = "",
    explanation: str = "",
    user_id: int = 0
) -> Dict[str, Any]:
    """Cleans up and saves a quick-add card from interactive examples."""
    cleaned_word = re.sub(r"^[^\w]+|[^\w]+$", "", word.strip())
    if cleaned_word:
        word = cleaned_word

    card_data = {
        "type": "vocab",
        "front": word,
        "back": translation or word,
        "transcription": transcription,
        "explanation": explanation or (f"Добавлено из примера: {sentence}" if sentence else "Добавлено пользователем"),
        "example": sentence,
        "pronunciation_text": word,
        "raw_original": f"{word} (из примера)"
    }
    card_id = db.add_card(card_data, user_id=user_id)
    card_data["id"] = card_id
    return card_data
