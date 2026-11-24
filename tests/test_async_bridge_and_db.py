"""
Tests for AsyncBridge concurrency and db_session transaction rollback/commit semantics.
"""

import asyncio
import threading
import pytest
import database as db
import app as web_app


class TestAsyncBridge:
    def test_async_bridge_executes_coroutine(self):
        bridge = web_app.AsyncBridge.get_instance()

        async def sample_coro(val):
            await asyncio.sleep(0.01)
            return val * 2

        result = bridge.run(sample_coro(21))
        assert result == 42

    def test_async_bridge_propagates_exceptions(self):
        bridge = web_app.AsyncBridge.get_instance()

        async def failing_coro():
            await asyncio.sleep(0.01)
            raise ValueError("Test error in async task")

        with pytest.raises(ValueError, match="Test error in async task"):
            bridge.run(failing_coro())

    def test_async_bridge_concurrent_calls(self):
        bridge = web_app.AsyncBridge.get_instance()
        results = []

        def worker(num):
            async def add(n):
                await asyncio.sleep(0.01)
                return n + 100

            res = bridge.run(add(num))
            results.append(res)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(10)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        assert len(results) == 10
        assert set(results) == set(range(100, 110))


class TestDbSessionTransactions:
    def test_db_session_commits_on_success(self, test_db):
        with db.db_session() as cursor:
            cursor.execute("INSERT INTO cards (front, back, type, next_review) VALUES (?, ?, ?, ?)",
                           ("persisted_front", "persisted_back", "vocab", "2026-01-01"))

        # In another session, verify row is committed
        with db.db_session() as cursor:
            cursor.execute("SELECT * FROM cards WHERE front = ?", ("persisted_front",))
            row = cursor.fetchone()
            assert row is not None
            assert row["back"] == "persisted_back"

    def test_db_session_rollback_on_exception(self, test_db):
        with pytest.raises(RuntimeError, match="Intentional failure"):
            with db.db_session() as cursor:
                cursor.execute("INSERT INTO cards (front, back, type, next_review) VALUES (?, ?, ?, ?)",
                               ("should_rollback", "will_be_discarded", "vocab", "2026-01-01"))
                raise RuntimeError("Intentional failure")

        # Verify row was rolled back and does not exist
        with db.db_session() as cursor:
            cursor.execute("SELECT * FROM cards WHERE front = ?", ("should_rollback",))
            assert cursor.fetchone() is None
