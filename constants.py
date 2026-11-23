"""
Global Constants for English Feedback Trainer
"""

CARD_TYPE_VOCAB = "vocab"
CARD_TYPE_CORRECTION = "correction"
CARD_TYPE_GOOD_LANGUAGE = "good_language"
CARD_TYPE_SUGGESTION = "suggestion"
CARD_TYPE_ANTONYM = "antonym"

CARD_TYPES = frozenset({
    CARD_TYPE_VOCAB,
    CARD_TYPE_CORRECTION,
    CARD_TYPE_GOOD_LANGUAGE,
    CARD_TYPE_SUGGESTION,
    CARD_TYPE_ANTONYM
})
