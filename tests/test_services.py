"""
Domain and Service Layer Tests: CardService, QuizService, and Active Recall Invariants
"""

import pytest
import database as db
from services import card_service, quiz_service


class TestCardService:
    def test_ingest_all_card_types(self, test_db):
        parsed = {
            "vocab": [
                {"word": "ubiquitous", "translation": "вездесущий", "transcription": "/juːˈbɪk.wɪ.təs/", "example": "Smartphones are ubiquitous.", "raw": "ubiquitous - вездесущий"}
            ],
            "corrections": [
                {"wrong": "he don't know", "correct": "he doesn't know", "quiz": "Исправь: he don't know?", "explanation": "3-е лицо ед. ч.", "raw": "he don't know -> he doesn't know"}
            ],
            "good_language": [
                {"phrase": "hit the ground running", "meaning": "начать с места в карьер", "example": "She hit the ground running.", "raw": "hit the ground running"}
            ],
            "suggestions": [
                {"basic": "very tired", "advanced": "exhausted", "quiz": "Как сказать вместо very tired?", "explanation": "Более выразительное слово", "raw": "very tired -> exhausted"}
            ]
        }

        total, counts = card_service.ingest_parsed_board(parsed, user_id=0)
        assert total == 4
        assert counts["vocab"] == 1
        assert counts["correction"] == 1
        assert counts["good_language"] == 1
        assert counts["suggestion"] == 1

        cards = db.get_all_cards(user_id=0)
        types = {c["type"] for c in cards}
        assert types == {"vocab", "correction", "good_language", "suggestion"}

    def test_ingest_empty_items_handling(self, test_db):
        parsed = {
            "vocab": [{"word": ""}, {"word": "   "}],
        }
        total, counts = card_service.ingest_parsed_board(parsed, user_id=0)
        assert total == 0
        assert counts["vocab"] == 0

    def test_quick_add_card_sanitization(self, test_db):
        # Punctuation stripping
        card = card_service.create_quick_add_card(
            word="...breathtaking!!",
            translation="захватывающий дух",
            sentence="The view was breathtaking.",
            user_id=0
        )
        assert card["front"] == "breathtaking"
        assert card["back"] == "захватывающий дух"
        assert "breathtaking" in card["example"]
        assert card["id"] > 0

    def test_quick_add_default_explanation(self, test_db):
        card = card_service.create_quick_add_card(word="simple", user_id=0)
        assert card["front"] == "simple"
        assert card["back"] == "simple"
        assert card["explanation"] == "Добавлено пользователем"


class TestQuizService:
    def test_quiz_returns_none_when_insufficient_cards(self, test_db):
        # 0 or 1 card -> None
        assert quiz_service.build_quiz_question(user_id=0) is None

        db.add_card({"front": "solo", "back": "одиночный", "type": "vocab"}, user_id=0)
        assert quiz_service.build_quiz_question(user_id=0) is None

    def test_quiz_with_sufficient_cards(self, sample_cards):
        quiz = quiz_service.build_quiz_question(user_id=0)
        assert quiz is not None
        assert "question" in quiz
        assert "correct_answer" in quiz
        assert len(quiz["options"]) >= 2
        assert quiz["correct_answer"] in quiz["options"]
        # All options in quiz must be unique
        assert len(quiz["options"]) == len(set(quiz["options"]))

    def test_antonym_quiz_generation(self, test_db):
        # Antonym quiz requires category pool to have >= 4 cards to prevent fallback to all cards
        pairs = [
            ("diligent ↔ lazy", "прилежный ↔ ленивый"),
            ("abundant ↔ scarce", "обильный ↔ скудный"),
            ("expand ↔ contract", "расширяться ↔ сжиматься"),
            ("vague ↔ distinct", "неясный ↔ отчетливый"),
        ]
        for front, back in pairs:
            db.add_card({"type": "antonym", "front": front, "back": back}, user_id=0)

        # Request category=antonym
        quiz = quiz_service.build_quiz_question(user_id=0, category="antonym")
        assert quiz is not None
        assert quiz["type"] == "antonym"
        assert "↔" in quiz["example"]
        assert quiz["correct_answer"] in quiz["options"]
        assert len(quiz["options"]) == 4

    def test_cloze_returns_none_when_no_cards(self, test_db):
        assert quiz_service.build_cloze_question(user_id=0) is None

    def test_cloze_masks_target_properly(self, sample_cards):
        cloze = quiz_service.build_cloze_question(user_id=0)
        assert cloze is not None
        assert "target" in cloze
        assert "masked_sentence" in cloze
        assert "__________" in cloze["masked_sentence"]

    def test_cloze_arrow_syntax_parsing(self, test_db):
        # Card with ➔
        db.add_card({
            "type": "correction",
            "front": "look at ➔ look after",
            "back": "заботиться",
            "example": "Please look after my cat.",
            "transcription": ""
        }, user_id=0)

        cloze = quiz_service.build_cloze_question(user_id=0)
        assert cloze is not None
        assert cloze["target"] == "look after"
        assert "__________" in cloze["masked_sentence"]
        assert "look after" not in cloze["masked_sentence"]
