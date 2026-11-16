import os
import sys
import threading
import time
import pytest
from pathlib import Path
from datetime import datetime, timedelta
import sqlite3

# Ensure english-feedback-bot root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import database

@pytest.fixture(autouse=True)
def setup_isolated_db(tmp_path, monkeypatch):
    """Sets up an isolated SQLite database file for each test."""
    test_db_path = tmp_path / "test_bot.db"
    monkeypatch.setattr(database, "DB_PATH", test_db_path)
    database.init_db()
    yield test_db_path
    try:
        if test_db_path.exists():
            test_db_path.unlink(missing_ok=True)
    except Exception:
        pass


# ==============================================================================
# 1. SQL INJECTION & PARAMETER INTEGRITY TESTS
# ==============================================================================

class TestSqlInjection:
    def test_sql_injection_in_add_card_fields(self):
        """Checks if malicious SQL payloads in text fields execute or get escaped."""
        payload = "test'; DROP TABLE cards; --"
        card_data = {
            "type": "vocab",
            "front": payload,
            "back": "' OR '1'='1",
            "explanation": "UNION SELECT 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15--",
            "example": "'); DELETE FROM cards WHERE '1'='1"
        }
        card_id = database.add_card(card_data)
        assert card_id is not None
        
        card = database.get_card_by_id(card_id)
        assert card is not None
        assert card["front"] == payload
        assert card["back"] == "' OR '1'='1"
        
        stats = database.get_stats()
        assert stats["total"] >= 1

    def test_sql_injection_in_get_due_cards_and_get_any_cards(self):
        """Tests SQL injection attempts in card_type filter."""
        database.add_card({"front": "word", "back": "meaning", "type": "vocab"})
        
        injection_type = "vocab' OR '1'='1"
        res_due = database.get_due_cards(card_type=injection_type)
        assert len(res_due) == 0

        res_any = database.get_any_cards(card_type=injection_type)
        assert len(res_any) == 0

    def test_sql_injection_or_malformed_limit(self):
        """Tests passing malformed limit."""
        with pytest.raises((TypeError, sqlite3.ProgrammingError, sqlite3.OperationalError)):
            database.get_due_cards(limit="10; DROP TABLE cards; --")

    def test_sql_injection_in_get_card_by_id(self):
        """Tests injection payload passed as card_id."""
        injection_id = "1 OR 1=1"
        card = database.get_card_by_id(injection_id)
        assert card is None


# ==============================================================================
# 2. SRS RATING LOGIC & BOUNDARY VULNERABILITY TESTS (FIXED & FORTIFIED)
# ==============================================================================

class TestSrsRatingVulnerabilities:
    def test_abnormal_ratings_rejected(self):
        """
        Verify that abnormal ratings (0, -999, 999) are strictly rejected
        and do not corrupt the card's interval or repetition.
        """
        cid = database.add_card({"front": "test", "back": "answer"})
        initial = database.get_card_by_id(cid)

        # Rating 0 is rejected
        res0 = database.update_srs_review(cid, rating=0)
        assert res0 == {}
        c0 = database.get_card_by_id(cid)
        assert c0["repetition"] == 0
        assert c0["interval"] == 0

        # Rating -999 is rejected
        res_neg = database.update_srs_review(cid, rating=-999)
        assert res_neg == {}
        c_neg = database.get_card_by_id(cid)
        assert c_neg["repetition"] == 0

        # Rating 999 is rejected
        res_high = database.update_srs_review(cid, rating=999)
        assert res_high == {}
        c_high = database.get_card_by_id(cid)
        assert c_high["repetition"] == 0

    def test_string_ratings_handled_safely(self):
        """Valid string '1', '2', '3' are converted; non-numeric strings are rejected."""
        cid = database.add_card({"front": "test", "back": "answer"})
        
        # Non-numeric string is rejected
        res_inv = database.update_srs_review(cid, rating="invalid")
        assert res_inv == {}
        
        # Valid string '1' is properly handled as rating 1 (Forgot)
        res_1 = database.update_srs_review(cid, rating="1")
        assert res_1 != {}
        c1 = database.get_card_by_id(cid)
        assert c1["repetition"] == 0
        assert c1["interval"] == 0

    def test_srs_interval_overflow_prevented_with_cap(self):
        """
        Checks that interval capping prevents OverflowError.
        """
        cid = database.add_card({"front": "overflow_test", "back": "answer"})
        
        # Even with extreme repetitions, interval is capped at MAX_INTERVAL_DAYS
        for _ in range(30):
            res = database.update_srs_review(cid, rating=3)
            assert res != {}
            assert res["interval_days"] <= database.MAX_INTERVAL_DAYS

        card = database.get_card_by_id(cid)
        assert card["interval"] <= database.MAX_INTERVAL_DAYS

    def test_ease_factor_bounds_and_float_drift(self):
        """Verify ease_factor limits (min 1.3, max 3.0)."""
        cid_min = database.add_card({"front": "ef_min_test", "back": "answer"})
        for _ in range(15):
            database.update_srs_review(cid_min, rating=1)
        card_min = database.get_card_by_id(cid_min)
        assert card_min["ease_factor"] == 1.3

        cid_max = database.add_card({"front": "ef_max_test", "back": "answer"})
        for _ in range(7):
            database.update_srs_review(cid_max, rating=3)
        card_max = database.get_card_by_id(cid_max)
        assert card_max["ease_factor"] == pytest.approx(3.0)

    def test_nonexistent_card_id_fails_silently(self):
        res = database.update_srs_review(999999, rating=1)
        assert res == {}


# ==============================================================================
# 3. EXTREME DATA, NULL VALUES & SPECIAL CHARACTERS
# ==============================================================================

class TestExtremeDataAndSpecialCharacters:
    def test_none_value_handled_gracefully(self):
        """add_card handles explicit None in front/back by defaulting to empty string."""
        malformed_card = {
            "type": "vocab",
            "front": None,
            "back": "valid back"
        }
        cid = database.add_card(malformed_card)
        card = database.get_card_by_id(cid)
        assert card["front"] == ""
        assert card["back"] == "valid back"

    def test_extreme_data_volume_large_strings(self):
        """Tests insertion and retrieval of large payloads (1MB text)."""
        large_text = "A" * (1024 * 1024)
        card_data = {
            "front": "large_front",
            "back": large_text,
            "explanation": large_text
        }
        cid = database.add_card(card_data)
        retrieved = database.get_card_by_id(cid)
        assert retrieved is not None
        assert len(retrieved["back"]) == 1024 * 1024

    def test_special_characters_emojis_html_and_null_bytes(self):
        """Tests unicode, emojis, control characters, and raw HTML."""
        special_payload = "English 🇬🇧 🚀 👨‍👩‍👧‍👦 \n\t\r <script>alert('xss')</script> \u202eRTL_OVERRIDE"
        card_data = {
            "front": special_payload,
            "back": "Back with quotes: '\"` and symbols: % & $ # @ !"
        }
        cid = database.add_card(card_data)
        retrieved = database.get_card_by_id(cid)
        assert retrieved["front"] == special_payload


# ==============================================================================
# 4. CONCURRENCY, DATA RACE & CONNECTION LEAKS
# ==============================================================================

class TestConcurrencyAndResourceLeaks:
    def test_connection_cleanup(self, tmp_path, monkeypatch):
        test_db = tmp_path / "leak_test.db"
        monkeypatch.setattr(database, "DB_PATH", test_db)
        database.init_db()

        # Database remains fully usable
        conn = database.get_connection()
        conn.execute("SELECT COUNT(*) FROM cards")
        conn.close()

    def test_atomic_update_prevents_race_conditions(self):
        """
        With atomic lock in update_srs_review, concurrent reviews are safely serialized.
        """
        cid = database.add_card({"front": "race_condition", "back": "answer"})
        num_threads = 5
        barrier = threading.Barrier(num_threads)
        errors = []

        def worker():
            try:
                barrier.wait()
                database.update_srs_review(cid, rating=2)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker) for _ in range(num_threads)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(errors) == 0
        final_card = database.get_card_by_id(cid)
        # All 5 reviews processed cleanly
        assert final_card["repetition"] == num_threads


# ==============================================================================
# 5. MULTI-USER ISOLATION TESTS (FIXED & ENFORCED)
# ==============================================================================

class TestMultiUserIsolation:
    def test_multi_user_isolation_enforced(self):
        """
        Ensures User A and User B cards are strictly isolated.
        """
        # User A adds a card
        card_a = database.add_card({
            "type": "correction",
            "front": "User A Private Error: I has a dog",
            "back": "I have a dog",
        }, user_id=1001)

        # User B queries cards
        user_b_cards = database.get_due_cards(user_id=2002, card_type="correction")
        assert len(user_b_cards) == 0

        # User B cannot see User A's card by ID
        assert database.get_card_by_id(card_a, user_id=2002) is None

        # User B cannot mutate User A's card
        res = database.update_srs_review(card_a, rating=1, user_id=2002)
        assert res == {}

        # User A can see their own card
        assert database.get_card_by_id(card_a, user_id=1001) is not None
