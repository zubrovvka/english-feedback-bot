"""
Batch import of cards from Miro board session dated 23.11.26
With strict deduplication against existing database.
"""

import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import database as db
from services import translation_service

db.init_db()

conn = db.get_connection()
cur = conn.cursor()
cur.execute("SELECT id, lower(front), lower(back), type FROM cards")
existing_rows = cur.fetchall()
conn.close()

def is_duplicate(candidate_front: str, candidate_type: str = "") -> bool:
    c_clean = re.sub(r"[^\w\s]", "", candidate_front.lower()).strip()
    for row in existing_rows:
        front_clean = re.sub(r"[^\w\s]", "", str(row[1]).lower()).strip()
        back_clean = re.sub(r"[^\w\s]", "", str(row[2]).lower()).strip()
        if c_clean == front_clean or c_clean == back_clean:
            return True
        # If one is substring and long enough
        if len(c_clean) > 8 and (c_clean in front_clean or front_clean in c_clean):
            if candidate_type and candidate_type == row[3]:
                return True
    return False

new_cards = [
    # ── GOOD LANGUAGE ──────────────────────────────────────────────────────────
    {
        "type": "good_language",
        "front": "I'm not going to",
        "back": "Я не собираюсь / не планирую...",
        "explanation": "Конструкция to be going to в отрицании для выражения намерения.",
        "example": "I'm not going to waste any more time.",
        "pronunciation_text": "I'm not going to"
    },
    {
        "type": "good_language",
        "front": "provide opportunities",
        "back": "предоставлять возможности",
        "explanation": "Отличная деловая коллокация: provide (а не give) opportunities.",
        "example": "This course will provide opportunities for career growth.",
        "pronunciation_text": "provide opportunities"
    },
    {
        "type": "good_language",
        "front": "area close to",
        "back": "район поблизости от / рядом с...",
        "explanation": "Используется предлог TO: close TO somewhere (не close from).",
        "example": "We rented an apartment in an area close to the city center.",
        "pronunciation_text": "area close to"
    },
    {
        "type": "good_language",
        "front": "explore",
        "back": "исследовать, изучать новое место / окрестности",
        "explanation": "Глагол для путешествий и прогулок: explore the city / area.",
        "example": "We had two days to explore the historical district.",
        "pronunciation_text": "explore"
    },
    {
        "type": "good_language",
        "front": "enjoy views",
        "back": "наслаждаться красивыми видами / пейзажем",
        "explanation": "Естественное выражение для путешествий: enjoy the views.",
        "example": "We sat on the terrace to enjoy the mountain views.",
        "pronunciation_text": "enjoy views"
    },
    {
        "type": "good_language",
        "front": "open your mind",
        "back": "расширять кругозор / быть открытым новому",
        "explanation": "Идиома: open one's mind (мыслить шире, избавиться от предубеждений).",
        "example": "Travelling to new cultures really helps open your mind.",
        "pronunciation_text": "open your mind"
    },
    {
        "type": "good_language",
        "front": "remind me",
        "back": "напомни мне / напоминает мне",
        "explanation": "Remind someone to do something (напомнить сделать) или remind of (напоминать о чем-то).",
        "example": "Please remind me to call the airport before departure.",
        "pronunciation_text": "remind me"
    },
    {
        "type": "good_language",
        "front": "extremely organized",
        "back": "чрезвычайно собранный / организованный",
        "explanation": "Сильное наречие extremely отлично усиливает прилагательное organized.",
        "example": "She is an extremely organized project manager.",
        "pronunciation_text": "extremely organized"
    },
    {
        "type": "good_language",
        "front": "I'm often late",
        "back": "Я часто опаздываю",
        "explanation": "To be late (быть опаздывающим). Наречие частоты often ставится после глагола to be.",
        "example": "I'm often late on Monday mornings because of traffic.",
        "pronunciation_text": "I'm often late"
    },
    {
        "type": "good_language",
        "front": "stay with my family",
        "back": "останавливаться / проводить время с семьей",
        "explanation": "To stay with somebody — гостить, проживать у кого-то.",
        "example": "Whenever I visit my hometown, I stay with my family.",
        "pronunciation_text": "stay with my family"
    },
    {
        "type": "good_language",
        "front": "get back in time",
        "back": "вернуться вовремя",
        "explanation": "In time — вовремя (с запасом времени), on time — строго по расписанию.",
        "example": "We need to get back in time for the meeting.",
        "pronunciation_text": "get back in time"
    },
    {
        "type": "good_language",
        "front": "start to think",
        "back": "начать задумываться / приходить к мысли",
        "explanation": "Start to think about something.",
        "example": "I start to think about taking a vacation.",
        "pronunciation_text": "start to think"
    },

    # ── CORRECTIONS ────────────────────────────────────────────────────────────
    {
        "type": "correction",
        "front": "Исправь ошибку: «my sis live with me»",
        "back": "My sis lives with me",
        "explanation": "В Present Simple для 3-го лица единственного числа (my sister = she) глагол получает окончание -s.",
        "example": "❌ my sis live with me ➔ ✅ My sister lives with me.",
        "pronunciation_text": "My sister lives with me"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «I'm not going to whip up something»",
        "back": "I'm not going to whip up anything",
        "explanation": "В отрицательных предложениях (not going to...) вместо something используется anything.",
        "example": "❌ not whip up something ➔ ✅ I'm not going to whip up anything.",
        "pronunciation_text": "I'm not going to whip up anything"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «Russian kitchen» (когда речь о блюдах)",
        "back": "Russian cuisine",
        "explanation": "Kitchen — это комната (кухня). Национальные блюда и кулинария — это cuisine (Russian cuisine, Italian cuisine).",
        "example": "❌ I love Russian kitchen ➔ ✅ I love Russian cuisine.",
        "pronunciation_text": "Russian cuisine"
    },
    {
        "type": "correction",
        "front": "Как перевести: «Когда две реки пересекаются...» (вариант 1)?",
        "back": "There are two rivers passing...",
        "explanation": "Passing through / crossing each other.",
        "example": "There are two rivers passing through this valley.",
        "pronunciation_text": "There are two rivers passing"
    },
    {
        "type": "correction",
        "front": "Как красиво сказать: «Когда две реки сливаются / пересекаются...» (вариант 2)?",
        "back": "When two rivers merge...",
        "explanation": "Merge — красивый точный глагол 'сливаться / объединяться' (о реках, дорогах, компаниях).",
        "example": "The city was founded where two rivers merge.",
        "pronunciation_text": "When two rivers merge"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «we was»",
        "back": "We were",
        "explanation": "Форма глагола to be в Past Simple для множественного числа (we / you / they) — WERE (не was).",
        "example": "❌ we was tired ➔ ✅ We were tired.",
        "pronunciation_text": "We were"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «I slept» (в значении 'я спал в тот момент, когда позвонили')",
        "back": "I was asleep / I was sleeping",
        "explanation": "Для описания состояния сна в определенный момент используется Past Continuous (I was sleeping) или состояние (I was asleep).",
        "example": "❌ I slept when you called ➔ ✅ I was asleep / I was sleeping when you called.",
        "pronunciation_text": "I was asleep"
    },
    {
        "type": "correction",
        "front": "Исправь ошибку: «management your time»",
        "back": "Manage your time",
        "explanation": "Нужен глагол в повелительном наклонении (manage), а не существительное (management).",
        "example": "❌ You should management your time ➔ ✅ You should manage your time.",
        "pronunciation_text": "Manage your time"
    },

    # ── SUGGESTIONS ────────────────────────────────────────────────────────────
    {
        "type": "suggestion",
        "front": "Как продвинуто сказать «начать новое занятие / хобби» вместо «start activity»?",
        "back": "take up",
        "explanation": "Фразовый глагол take up означает начать регулярно заниматься хобби, спортом или активностью (take up tennis / painting).",
        "example": "I decided to take up swimming this winter.",
        "pronunciation_text": "take up"
    },
    {
        "type": "suggestion",
        "front": "Какими словами заменить «nervous», когда говоришь о раздражающей ситуации или поведении?",
        "back": "irritating / annoying",
        "explanation": "Nervous описывает нервозность человека. Раздражающие вещи или поведение — это irritating или annoying.",
        "example": "That loud noise is really irritating and annoying.",
        "pronunciation_text": "irritating and annoying"
    },

    # ── PRONUNCIATION & VOCAB ──────────────────────────────────────────────────
    {
        "type": "vocab",
        "front": "cathedral",
        "back": "собор, кафедральный собор",
        "transcription": "/kəˈθiː.drəl/",
        "explanation": "Обрати внимание на ударение на второй слог и звук /θ/: cathedral.",
        "example": "We visited the ancient cathedral in the city center.",
        "pronunciation_text": "cathedral"
    },
    {
        "type": "vocab",
        "front": "generation",
        "back": "поколение",
        "transcription": "/ˌdʒen.əˈreɪ.ʃən/",
        "explanation": "All the people of about the same age within a society.",
        "example": "The younger generation is very tech-savvy.",
        "pronunciation_text": "generation"
    },
    {
        "type": "vocab",
        "front": "museum",
        "back": "музей",
        "transcription": "/mjuːˈziː.əm/",
        "explanation": "Ударение на второй слог: mu-SE-um /mjuːˈziː.əm/.",
        "example": "Admission to the museum is free on Sundays.",
        "pronunciation_text": "museum"
    },
    {
        "type": "vocab",
        "front": "hit the shops",
        "back": "пройтись по магазинам, заняться шопингом",
        "transcription": "/hɪt ðə ʃɒps/",
        "explanation": "Разговорная идиома: to hit the shops = to go shopping.",
        "example": "After lunch, we decided to hit the shops to find some new clothes.",
        "pronunciation_text": "hit the shops"
    },
    {
        "type": "vocab",
        "front": "a bookcase",
        "back": "книжный шкаф / полка для книг",
        "transcription": "/ˈbʊk.keɪs/",
        "explanation": "A piece of furniture with shelves used for storing books.",
        "example": "He put the novel back on the bookcase.",
        "pronunciation_text": "a bookcase"
    },
    {
        "type": "vocab",
        "front": "a novel",
        "back": "роман (художественная книга)",
        "transcription": "/ˈnɒv.əl/",
        "explanation": "A long printed story about imaginary characters and events.",
        "example": "Have you read any of Jane Austen's novels?",
        "pronunciation_text": "a novel"
    },
    {
        "type": "vocab",
        "front": "pick up",
        "back": "забрать, заехать за кем-то / подобрать",
        "transcription": "/pɪk ʌp/",
        "explanation": "To collect, or to go and get someone or something.",
        "example": "Could you pick up the children after school?",
        "pronunciation_text": "pick up"
    },
    {
        "type": "vocab",
        "front": "be tolerant with sb",
        "back": "быть терпимым / толерантным к кому-то",
        "transcription": "/biː ˈtɒl.ər.ənt wɪð/",
        "explanation": "To be accepting and patient with people who have different views or habits.",
        "example": "We should be tolerant with people whose opinions differ from ours.",
        "pronunciation_text": "be tolerant with somebody"
    },
    {
        "type": "vocab",
        "front": "reflect on",
        "back": "размышлять о чем-то, обдумывать",
        "transcription": "/rɪˈflekt ɒn/",
        "explanation": "To think deeply or carefully about something.",
        "example": "He took a moment to reflect on what had happened.",
        "pronunciation_text": "reflect on"
    },
    {
        "type": "vocab",
        "front": "The person makes the place",
        "back": "Не место красит человека, а человек место",
        "explanation": "Полная пословица: It's not the place that makes the person, it's the person who makes the place.",
        "example": "Remember: the person makes the place, not the other way around.",
        "pronunciation_text": "The person makes the place"
    },
    {
        "type": "vocab",
        "front": "Church of the Savior on the Spilled Blood",
        "back": "Храм Спаса на Крови (в Санкт-Петербурге)",
        "transcription": "/tʃɜːtʃ əv ðə ˈseɪv.jər ɒn ðə spɪld blʌd/",
        "explanation": "Знаменитый исторический собор с мозаиками в Санкт-Петербурге.",
        "example": "The Church of the Savior on the Spilled Blood is famous for its colorful domes.",
        "pronunciation_text": "Church of the Savior on the Spilled Blood"
    },

    # ── PREPOSITION COLLOCATIONS (Green sticky notes) ───────────────────────────
    {
        "type": "vocab",
        "front": "arrive in",
        "back": "прибывать в город / страну (arrive in London, arrive in Spain)",
        "explanation": "С городами и странами используется предлог IN (не at).",
        "example": "We arrived in Paris late in the evening.",
        "pronunciation_text": "arrive in"
    },
    {
        "type": "vocab",
        "front": "arrive at",
        "back": "прибывать в конкретное здание / место (arrive at the airport/station)",
        "explanation": "С конкретными точками, зданиями, вокзалами и аэропортами используется предлог AT.",
        "example": "What time did you arrive at the airport?",
        "pronunciation_text": "arrive at"
    },
    {
        "type": "vocab",
        "front": "depend on",
        "back": "зависеть от кого-то / чего-то",
        "explanation": "После depend ВСЕГДА используется предлог ON (не from!).",
        "example": "Our plans depend on the weather tomorrow.",
        "pronunciation_text": "depend on"
    },
    {
        "type": "vocab",
        "front": "pay for",
        "back": "платить за что-то (pay for dinner / the tickets)",
        "explanation": "Когда указываешь, за ЧТО платишь, нужен предлог FOR.",
        "example": "Let me pay for the coffee today.",
        "pronunciation_text": "pay for"
    },
    {
        "type": "vocab",
        "front": "worry about",
        "back": "беспокоиться / переживать о чем-то",
        "explanation": "Коллокация с предлогом ABOUT: worry about something.",
        "example": "Don't worry about things you cannot change.",
        "pronunciation_text": "worry about"
    },
    {
        "type": "vocab",
        "front": "think about",
        "back": "думать о ком-то/чем-то (размышлять, взвешивать)",
        "explanation": "Think about — процесс обдумывания или мысли о ком-то.",
        "example": "I need some time to think about your proposal.",
        "pronunciation_text": "think about"
    },
    {
        "type": "vocab",
        "front": "belong to",
        "back": "принадлежать кому-то",
        "explanation": "После belong ВСЕГДА идет предлог TO (не for / not with).",
        "example": "Does this leather jacket belong to you?",
        "pronunciation_text": "belong to"
    },
    {
        "type": "vocab",
        "front": "ask for",
        "back": "просить что-то (ask for help / directions / advice)",
        "explanation": "Ask someone (спросить кого-то), но ask FOR something (попросить что-то).",
        "example": "Never hesitate to ask for help if you need it.",
        "pronunciation_text": "ask for"
    },
    {
        "type": "vocab",
        "front": "agree with",
        "back": "соглашаться с кем-то / чьим-то мнением",
        "explanation": "Agree WITH somebody. В английском это глагол (не 'I am agree', а 'I agree').",
        "example": "I completely agree with your assessment.",
        "pronunciation_text": "agree with"
    },
    {
        "type": "vocab",
        "front": "listen to",
        "back": "слушать кого-то / что-то (listen to music / podcasts)",
        "explanation": "После глагола listen ВСЕГДА ставится предлог TO перед объектом.",
        "example": "I like to listen to podcasts on my commute.",
        "pronunciation_text": "listen to"
    },
    {
        "type": "vocab",
        "front": "speak to",
        "back": "разговаривать с кем-то (speak to the manager)",
        "explanation": "Speak TO somebody (или with).",
        "example": "May I speak to the doctor, please?",
        "pronunciation_text": "speak to"
    },
    {
        "type": "vocab",
        "front": "believe in",
        "back": "верить в кого-то / что-то (believe in yourself)",
        "explanation": "Коллокация: believe IN sb/sth.",
        "example": "You have to believe in yourself to succeed.",
        "pronunciation_text": "believe in"
    },
    {
        "type": "vocab",
        "front": "think of",
        "back": "иметь мнение о / придумать мысль",
        "explanation": "What do you think OF... (каково твое мнение о...). Также 'вспомнить': I can't think of his name.",
        "example": "What do you think of our new English teacher?",
        "pronunciation_text": "think of"
    },
    {
        "type": "vocab",
        "front": "speak about",
        "back": "говорить / выступать на какую-то тему",
        "explanation": "Speak about a topic or issue.",
        "example": "She will speak about artificial intelligence at the conference.",
        "pronunciation_text": "speak about"
    },
    {
        "type": "vocab",
        "front": "stressed about",
        "back": "испытывающий стресс из-за чего-то",
        "explanation": "Прилагательное stressed + предлог ABOUT.",
        "example": "He was very stressed about his upcoming exam.",
        "pronunciation_text": "stressed about"
    },
    {
        "type": "vocab",
        "front": "immediate success",
        "back": "мгновенный / немедленный успех",
        "explanation": "Устойчивое словосочетание: immediate success.",
        "example": "The new product was an immediate success in the market.",
        "pronunciation_text": "immediate success"
    }
]

added_count = 0
skipped_count = 0

for card in new_cards:
    if is_duplicate(card["front"], card["type"]):
        skipped_count += 1
        print(f"  ⚠️  Skipped (duplicate): {card['front']}")
    else:
        # Pre-translate card if sentence translation is helpful
        trans = translation_service.get_or_create_card_translation(card)
        if trans:
            card["translation"] = trans
        db.add_card(card, user_id=0)
        added_count += 1
        print(f"  ✅ Added [{card['type']}]: {card['front']}")

print(f"\n{'='*50}")
print(f"Done! Added: {added_count}, Skipped duplicates: {skipped_count}")

all_cards = db.get_all_cards(limit=9999)
print(f"Total cards in DB now: {len(all_cards)}")
