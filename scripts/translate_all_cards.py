"""
Pre-translates all cards that do not have a Russian sentence translation.
"""

import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from services import translation_service

db.init_db()

conn = db.get_connection()
cur = conn.cursor()
cur.execute("""
    SELECT * FROM cards 
    WHERE (translation IS NULL OR translation = '')
    ORDER BY id ASC
""")
rows = [dict(r) for r in cur.fetchall()]
conn.close()

print(f"Total cards to check/translate: {len(rows)}")

translated_count = 0
for i, card in enumerate(rows):
    trans = translation_service.get_or_create_card_translation(card)
    if trans:
        translated_count += 1
        if translated_count % 25 == 0 or translated_count <= 5:
            print(f"[{i+1}/{len(rows)}] #{card['id']} ({card['type']}): '{card.get('back') or card.get('front')}' -> '{trans}'")
    time.sleep(0.04)

print(f"\nDone! Successfully translated and cached {translated_count} cards.")
