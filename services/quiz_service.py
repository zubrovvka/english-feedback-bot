"""
Quiz & Active Recall Service
Provides logic for:
1. 4-Option Multiple Choice Quizzes with dynamic distractors.
2. Cloze Deletion (Fill-in-the-blank) sentence masking.
"""

import random
import re
from typing import Optional, Dict, Any
import database as db


def build_quiz_question(user_id: int = 0, category: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Generates a 4-choice quiz question with realistic distractors."""
    if category in ("", "all", "None"):
        category = None

    pool = db.get_any_cards(user_id=user_id, card_type=category, limit=25)
    if len(pool) < 4:
        pool = db.get_any_cards(user_id=user_id, limit=25)

    if len(pool) < 2:
        return None

    target = pool[0]
    # Filter distractors with unique back and front
    distractors = [c for c in pool[1:] if c["back"] != target["back"] and c["front"] != target["front"]]
    random.shuffle(distractors)
    chosen = distractors[:3]

    options = [target["back"]] + [d["back"] for d in chosen]
    random.shuffle(options)

    return {
        "card_id": target["id"],
        "type": target["type"],
        "question": target["front"],
        "transcription": target.get("transcription", ""),
        "correct_answer": target["back"],
        "options": options,
        "example": target.get("example", ""),
        "explanation": target.get("explanation", "")
    }


def build_cloze_question(user_id: int = 0, category: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """Generates a fill-in-the-blank cloze question from due or available cards."""
    if category in ("", "all", "None"):
        category = None

    cards = db.get_due_cards(user_id=user_id, card_type=category, limit=10)
    if not cards:
        cards = db.get_any_cards(user_id=user_id, card_type=category, limit=10)

    if not cards:
        return None

    # Prefer cards with an example sentence
    card = next((c for c in cards if c.get("example") and len(c.get("example", "")) > 10), cards[0])
    
    front = card.get("front", "").strip()
    back = card.get("back", "").strip()
    sentence = card.get("example") or ""
    
    # Identify target phrase to mask
    if "➔" in front:
        target = front.split("➔")[1].strip()
    elif "->" in front:
        target = front.split("->")[1].strip()
    elif card.get("type") == "vocab":
        target = front
    elif card.get("type") in ("good_language", "suggestion"):
        target = back if len(back) < 35 else front
    else:
        target = back or front

    # Clean target
    clean_target = re.sub(r"^[a-zA-Z]\)\s*", "", target).strip()
    clean_target = re.sub(r"\[.*?\]|\(.*?\)", "", clean_target).strip()

    masked_sentence = ""
    if sentence and clean_target:
        # Case insensitive replace of first occurrence
        pattern = re.compile(re.escape(clean_target), re.IGNORECASE)
        if pattern.search(sentence):
            masked_sentence = pattern.sub("__________", sentence, count=1)

    if not masked_sentence:
        if sentence:
            masked_sentence = f"{sentence} (целевое слово: __________)"
        else:
            masked_sentence = f"Как сказать: «{back}»? [__________]"

    return {
        "card_id": card["id"],
        "type": card["type"],
        "target": clean_target,
        "masked_sentence": masked_sentence,
        "full_sentence": sentence,
        "hint": back,
        "explanation": card.get("explanation", ""),
        "transcription": card.get("transcription", "")
    }
