import sqlite3
import threading
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from config import DB_PATH

# Thread lock for atomic operations in multithreaded / concurrent scenarios
_db_lock = threading.Lock()

MAX_INTERVAL_DAYS = 365  # Cap interval to 1 year to prevent exponential explosion

def get_connection():
    conn = sqlite3.connect(DB_PATH, timeout=20.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS cards (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL DEFAULT 0,
            type TEXT NOT NULL, -- 'vocab', 'correction', 'good_language', 'suggestion'
            front TEXT NOT NULL,
            back TEXT NOT NULL,
            explanation TEXT,
            example TEXT,
            transcription TEXT,
            pronunciation_text TEXT,
            raw_original TEXT,
            ease_factor REAL DEFAULT 2.5,
            interval INTEGER DEFAULT 0,
            repetition INTEGER DEFAULT 0,
            next_review TIMESTAMP NOT NULL,
            lesson_date TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Check if user_id column exists (for backward compatibility / migrations)
        cursor.execute("PRAGMA table_info(cards)")
        columns = [row[1] for row in cursor.fetchall()]
        if "user_id" not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN user_id INTEGER NOT NULL DEFAULT 0")
        if "translation" not in columns:
            cursor.execute("ALTER TABLE cards ADD COLUMN translation TEXT DEFAULT ''")
            
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cards_user_next ON cards (user_id, next_review)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_cards_user_type ON cards (user_id, type)")
        conn.commit()
    finally:
        conn.close()

def add_card(card_data: Dict[str, Any], user_id: int = 0) -> int:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        now = datetime.now()
        next_review = now.isoformat()
        
        front = card_data.get('front', '')
        back = card_data.get('back', '')
        if front is None:
            front = ''
        if back is None:
            back = ''
            
        card_type = card_data.get('type', 'vocab') or 'vocab'
        
        cursor.execute("""
        INSERT INTO cards (
            user_id, type, front, back, explanation, example, transcription,
            pronunciation_text, raw_original, ease_factor, interval,
            repetition, next_review, lesson_date, created_at, translation
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_id,
            card_type,
            front,
            back,
            card_data.get('explanation') or '',
            card_data.get('example') or '',
            card_data.get('transcription') or '',
            card_data.get('pronunciation_text') or front,
            card_data.get('raw_original') or '',
            2.5,
            0,
            0,
            next_review,
            card_data.get('lesson_date', now.strftime("%Y-%m-%d")),
            now.isoformat(),
            card_data.get('translation') or ''
        ))
        card_id = cursor.lastrowid
        conn.commit()
        return card_id
    finally:
        conn.close()

def get_due_cards(user_id: int = 0, card_type: Optional[str] = None, limit: int = 20) -> List[Dict[str, Any]]:
    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer")
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        now_str = datetime.now().isoformat()
        
        if card_type:
            cursor.execute("""
            SELECT * FROM cards 
            WHERE user_id = ? AND type = ? AND next_review <= ?
            ORDER BY next_review ASC
            LIMIT ?
            """, (user_id, card_type, now_str, limit))
        else:
            cursor.execute("""
            SELECT * FROM cards 
            WHERE user_id = ? AND next_review <= ?
            ORDER BY next_review ASC
            LIMIT ?
            """, (user_id, now_str, limit))
            
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_any_cards(user_id: int = 0, card_type: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
    if not isinstance(limit, int):
        raise TypeError("Limit must be an integer")
        
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        if card_type:
            cursor.execute("""
            SELECT * FROM cards 
            WHERE user_id = ? AND type = ?
            ORDER BY RANDOM()
            LIMIT ?
            """, (user_id, card_type, limit))
        else:
            cursor.execute("""
            SELECT * FROM cards 
            WHERE user_id = ?
            ORDER BY RANDOM()
            LIMIT ?
            """, (user_id, limit))
            
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def get_card_by_id(card_id: Any, user_id: Optional[int] = None) -> Optional[Dict[str, Any]]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if user_id is not None:
            cursor.execute("SELECT * FROM cards WHERE id = ? AND user_id = ?", (card_id, user_id))
        else:
            cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    finally:
        conn.close()

def update_srs_review(card_id: int, rating: Any, user_id: Optional[int] = None) -> Dict[str, Any]:
    """
    SuperMemo-2 style spaced repetition update with validation, atomic lock and bounds checking.
    Valid ratings:
      1 = Forgot / Wrong
      2 = Hard / Hesitated
      3 = Good / Easy
    """
    # Strict rating validation (guards against rating fallthrough / type confusion)
    try:
        rating_int = int(rating)
    except (ValueError, TypeError):
        return {}
        
    if rating_int not in (1, 2, 3):
        return {}

    with _db_lock:
        conn = get_connection()
        try:
            cursor = conn.cursor()
            if user_id is not None:
                cursor.execute("SELECT * FROM cards WHERE id = ? AND user_id = ?", (card_id, user_id))
            else:
                cursor.execute("SELECT * FROM cards WHERE id = ?", (card_id,))
            row = cursor.fetchone()
            if not row:
                return {}
                
            card = dict(row)
            interval = card['interval']
            repetition = card['repetition']
            ease_factor = card['ease_factor']
            
            now = datetime.now()
            
            if rating_int == 1:
                # Forgot
                repetition = 0
                interval = 0
                next_review = now + timedelta(minutes=10)
                ease_factor = max(1.3, ease_factor - 0.2)
            elif rating_int == 2:
                # Hard
                if repetition == 0:
                    interval = 1
                else:
                    interval = max(1, int(interval * 1.2))
                repetition += 1
                interval = min(interval, MAX_INTERVAL_DAYS)
                next_review = now + timedelta(days=interval)
                ease_factor = max(1.3, ease_factor - 0.1)
            else:
                # Good / Easy (3)
                if repetition == 0:
                    interval = 1
                elif repetition == 1:
                    interval = 3
                else:
                    interval = int(interval * ease_factor)
                repetition += 1
                interval = min(interval, MAX_INTERVAL_DAYS)
                next_review = now + timedelta(days=interval)
                ease_factor = min(3.0, ease_factor + 0.1)
                
            cursor.execute("""
            UPDATE cards SET
                ease_factor = ?,
                interval = ?,
                repetition = ?,
                next_review = ?
            WHERE id = ?
            """, (ease_factor, interval, repetition, next_review.isoformat(), card_id))
            conn.commit()
            
            return {
                "interval_days": interval,
                "next_review": next_review.strftime("%d.%m %H:%M")
            }
        finally:
            conn.close()

def get_stats(user_id: int = 0) -> Dict[str, Any]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM cards WHERE user_id = ?", (user_id,))
        total_cards = cursor.fetchone()[0]
        
        now_str = datetime.now().isoformat()
        cursor.execute("SELECT COUNT(*) FROM cards WHERE user_id = ? AND next_review <= ?", (user_id, now_str))
        due_cards = cursor.fetchone()[0]
        
        cursor.execute("""
        SELECT type, COUNT(*) as count 
        FROM cards 
        WHERE user_id = ?
        GROUP BY type
        """, (user_id,))
        by_type = {row['type']: row['count'] for row in cursor.fetchall()}
        
        return {
            "total": total_cards,
            "due": due_cards,
            "by_type": by_type
        }
    finally:
        conn.close()

def get_all_cards(user_id: int = 0, limit: int = 200) -> List[Dict[str, Any]]:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        SELECT * FROM cards 
        WHERE user_id = ?
        ORDER BY id DESC
        LIMIT ?
        """, (user_id, limit))
        rows = cursor.fetchall()
        return [dict(row) for row in rows]
    finally:
        conn.close()

def delete_card(card_id: int, user_id: Optional[int] = None) -> bool:
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if user_id is not None:
            cursor.execute("DELETE FROM cards WHERE id = ? AND user_id = ?", (card_id, user_id))
        else:
            cursor.execute("DELETE FROM cards WHERE id = ?", (card_id,))
        conn.commit()
        return cursor.rowcount > 0
    finally:
        conn.close()
