"""
Telegram Bot (Decommissioned)
This project has transitioned completely to the standalone Web Application (English Feedback Trainer).
This file retains BoundedSessionStorage for backward compatibility.
"""

import sys
import time
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)

class BoundedSessionStorage:
    """Bounded session storage with TTL to prevent memory leaks (preserved utility)."""
    def __init__(self, max_size: int = 1000, ttl_seconds: int = 7200):
        self.max_size = max_size
        self.ttl = ttl_seconds
        self.sessions: Dict[int, Dict[str, Any]] = {}

    def get(self, user_id: int) -> Dict[str, Any]:
        self.cleanup_expired_sessions()
        return self.sessions.get(user_id, {})

    def set(self, user_id: int, card_id: int, category: Optional[str]):
        self.cleanup_expired_sessions()
        if len(self.sessions) >= self.max_size:
            oldest_key = min(self.sessions.keys(), key=lambda k: self.sessions[k].get("timestamp", 0))
            self.sessions.pop(oldest_key, None)
            
        self.sessions[user_id] = {
            "current_card_id": card_id,
            "category": category,
            "timestamp": time.time()
        }

    def cleanup_expired_sessions(self):
        now = time.time()
        expired = [uid for uid, s in self.sessions.items() if now - s.get("timestamp", 0) > self.ttl]
        for uid in expired:
            self.sessions.pop(uid, None)

    def clear(self):
        self.sessions.clear()

    def __getitem__(self, user_id: int):
        return self.get(user_id)

    def __setitem__(self, user_id: int, value: Dict[str, Any]):
        self.set(user_id, value.get("current_card_id", 0), value.get("category"))

    def __len__(self):
        return len(self.sessions)

USER_SESSIONS = BoundedSessionStorage()

def main():
    print("=" * 60)
    print(" [!] Telegram-бот выведен из эксплуатации.")
    print(" [!] Приложение полностью переведено на Web-тренажер.")
    print(" [*] Запуск Web-сервера: python app.py")
    print("=" * 60)
    from app import main as run_web_app
    run_web_app()

if __name__ == "__main__":
    main()
