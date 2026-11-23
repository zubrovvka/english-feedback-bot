"""
Migration: Tag cards with antonym pairs as type 'antonym'
and configure their pronunciation text to the prompt word.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import database as db

db.init_db()

conn = db.get_connection()
cur = conn.cursor()

cur.execute("""
    SELECT id, front, back, transcription 
    FROM cards 
    WHERE front LIKE '%↔%' OR front LIKE '%<->%'
""")
rows = [dict(r) for r in cur.fetchall()]

print(f"Found {len(rows)} antonym pair cards to upgrade:")

for r in rows:
    front = r['front']
    delim = '↔' if '↔' in front else '<->'
    parts = [p.strip() for p in front.split(delim)]
    if len(parts) == 2:
        w1, w2 = parts
        cur.execute("""
            UPDATE cards 
            SET type = 'antonym',
                pronunciation_text = ?
            WHERE id = ?
        """, (w1, r['id']))
        print(f"  ⚡ Card #{r['id']}: '{w1}' ↔ '{w2}' (type=antonym, speech='{w1}')")

conn.commit()
conn.close()
print("Antonym migration complete!")
