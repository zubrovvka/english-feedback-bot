import asyncio
import html
import logging
import time
from pathlib import Path
from typing import Optional, Dict, Any

from aiogram import Bot, Dispatcher, F, types, BaseMiddleware
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    FSInputFile
)
from aiogram.utils.keyboard import InlineKeyboardBuilder

import config
import database as db
import gemini_parser
import tts_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

bot: Optional[Bot] = None
dp = Dispatcher()

# Bounded session storage with TTL to prevent memory leaks
# user_id -> {"current_card_id": int, "category": Optional[str], "timestamp": float}
class BoundedSessionStorage:
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
            # Evict oldest
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

# Security Whitelist Middleware
class WhitelistMiddleware(BaseMiddleware):
    async def __call__(self, handler, event: types.TelegramObject, data: Dict[str, Any]):
        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)
            
        allowed_ids = config.ALLOWED_USER_IDS
        if allowed_ids and user.id not in allowed_ids:
            logger.warning(f"Unauthorized access attempt from user_id: {user.id} (@{user.username})")
            if isinstance(event, types.Message):
                await event.answer(
                    "⛔ <b>Доступ ограничен.</b>\n"
                    "Этот бот настроен строго для персонального использования владельцем.",
                    parse_mode="HTML"
                )
            elif isinstance(event, types.CallbackQuery):
                await event.answer("⛔ Доступ ограничен.", show_alert=True)
            return

        return await handler(event, data)

dp.message.middleware(WhitelistMiddleware())
dp.callback_query.middleware(WhitelistMiddleware())

def get_main_reply_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🚀 Учить карточки"), KeyboardButton(text="📊 Моя статистика")],
            [KeyboardButton(text="🔤 Новые слова"), KeyboardButton(text="❌ Разбор ошибок")],
            [KeyboardButton(text="⭐ Закрепление лексики"), KeyboardButton(text="ℹ️ Помощь")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    user_id = message.from_user.id
    
    # Check if ALLOWED_USER_IDS is configured
    id_note = ""
    if not config.ALLOWED_USER_IDS:
        id_note = (
            f"\n\n🔐 <b>Твой Telegram ID:</b> <code>{user_id}</code>\n"
            "Чтобы заблокировать бота от посторонних, добавь этот ID в файл <code>.env</code>:\n"
            f"<code>ALLOWED_USER_IDS={user_id}</code>"
        )
        
    welcome_text = (
        "👋 <b>Привет, бро!</b>\n\n"
        "Я твой персональный тренажер английского.\n\n"
        "📸 <b>Как это работает:</b>\n"
        "После урока с репетитором просто <b>скинь мне скриншот доски Miro</b>.\n"
        "Я сам:\n"
        "1. Распознаю все колонки (<code>New vocab</code>, <code>Corrections</code>, <code>Good language</code>, <code>Suggestions</code>).\n"
        "2. Разложу всё по карточкам с переводом, транскрипцией и примерами.\n"
        "3. Добавлю правильное британское/американское произношение.\n"
        "4. Запущу интервальное повторение, чтобы ничего не забывалось.\n\n"
        "Жми <b>🚀 Учить карточки</b> или отправь мне фото с урока прямо сейчас!"
        f"{id_note}"
    )
    await message.answer(welcome_text, parse_mode="HTML", reply_markup=get_main_reply_keyboard())

@dp.message(F.text == "ℹ️ Помощь")
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    help_text = (
        "📖 <b>Инструкция по использованию:</b>\n\n"
        "1. <b>Скриншот доски:</b> Просто прикрепи и отправь фото доски Miro после занятия.\n"
        "2. <b>🔤 Новые слова:</b> Режим как в ReWord — слово, транскрипция, перевод, пример и озвучка.\n"
        "3. <b>❌ Разбор ошибок:</b> Интерактивный тест — покажет типичную ошибку и предложит вспомнить, как сказать правильно.\n"
        "4. <b>⭐ Закрепление лексики:</b> Тренировка удачных фраз с урока, чтобы они вошли в привычку.\n"
        "5. <b>🔊 Озвучка:</b> В любой карточке нажми кнопку «Озвучка», чтобы послушать произношение носителя."
    )
    await message.answer(help_text, parse_mode="HTML")

@dp.message(F.text == "📊 Моя статистика")
@dp.message(Command("stats"))
async def cmd_stats(message: types.Message):
    user_id = message.from_user.id
    stats = db.get_stats(user_id=user_id)
    by_type = stats.get("by_type", {})
    text = (
        "📊 <b>Твоя статистика знаний:</b>\n\n"
        f"📚 Всего карточек в базе: <b>{stats['total']}</b>\n"
        f"⏰ Ждут повторения сегодня: <b>{stats['due']}</b>\n\n"
        "<b>По категориям:</b>\n"
        f"• 🔤 Новые слова: <b>{by_type.get('vocab', 0)}</b>\n"
        f"• ❌ Исправленные ошибки: <b>{by_type.get('correction', 0)}</b>\n"
        f"• ⭐ Закрепленная лексика: <b>{by_type.get('good_language', 0)}</b>\n"
        f"• 💡 Улучшайзеры: <b>{by_type.get('suggestion', 0)}</b>\n"
    )
    await message.answer(text, parse_mode="HTML")

# Handle photo uploads (Miro screenshots)
@dp.message(F.photo)
async def handle_photo(message: types.Message):
    user_id = message.from_user.id
    if not config.GEMINI_API_KEY:
        await message.answer("⚠️ Не настроен <code>GEMINI_API_KEY</code>. Укажи его в файле <code>.env</code>.", parse_mode="HTML")
        return

    status_msg = await message.answer("🔍 <b>Сканирую скриншот доски...</b>\nРаспознаю колонки, ошибки и новые слова...", parse_mode="HTML")
    
    try:
        photo = message.photo[-1]
        file_info = await bot.get_file(photo.file_id)
        
        temp_img_path = config.DATA_DIR / f"temp_{photo.file_id}.png"
        await bot.download_file(file_info.file_path, destination=temp_img_path)
        
        # Parse via Gemini
        parsed_data = await gemini_parser.parse_board_image(temp_img_path, config.GEMINI_API_KEY)
        
        # Cleanup temp file
        if temp_img_path.exists():
            temp_img_path.unlink()
            
        # Save to DB scoped by user_id
        vocab_items = parsed_data.get("vocab", [])
        corrections = parsed_data.get("corrections", [])
        good_lang = parsed_data.get("good_language", [])
        suggestions = parsed_data.get("suggestions", [])
        
        added_count = 0
        
        # 1. Vocab
        for item in vocab_items:
            db.add_card({
                "type": "vocab",
                "front": item.get("word", ""),
                "back": item.get("translation", ""),
                "transcription": item.get("transcription", ""),
                "example": item.get("example", ""),
                "pronunciation_text": item.get("word", ""),
                "raw_original": item.get("raw", "")
            }, user_id=user_id)
            added_count += 1
            
        # 2. Corrections
        for item in corrections:
            db.add_card({
                "type": "correction",
                "front": item.get("quiz", f"Как сказать правильно: {item.get('wrong')}?"),
                "back": item.get("correct", ""),
                "explanation": item.get("explanation", ""),
                "example": f"❌ {item.get('wrong')} ➔ ✅ {item.get('correct')}",
                "pronunciation_text": item.get("correct", ""),
                "raw_original": item.get("raw", "")
            }, user_id=user_id)
            added_count += 1
            
        # 3. Good Language
        for item in good_lang:
            db.add_card({
                "type": "good_language",
                "front": f"Вспомни выражение: «{item.get('meaning', item.get('phrase'))}»",
                "back": item.get("phrase", ""),
                "explanation": item.get("meaning", ""),
                "example": item.get("example", ""),
                "pronunciation_text": item.get("phrase", ""),
                "raw_original": item.get("raw", "")
            }, user_id=user_id)
            added_count += 1
            
        # 4. Suggestions
        for item in suggestions:
            db.add_card({
                "type": "suggestion",
                "front": item.get("quiz", f"Как сказать более продвинуто вместо: «{item.get('basic')}»?"),
                "back": item.get("advanced", ""),
                "explanation": item.get("explanation", ""),
                "example": f"Вместо «{item.get('basic')}» лучше: {item.get('advanced')}",
                "pronunciation_text": item.get("advanced", ""),
                "raw_original": item.get("raw", "")
            }, user_id=user_id)
            added_count += 1
            
        builder = InlineKeyboardBuilder()
        builder.button(text="🚀 Начать учить этот урок", callback_data="start_learn_all")
        
        summary_text = (
            "✅ <b>Доска успешно обработана!</b>\n\n"
            f"📥 Всего сохранено карточек: <b>{added_count}</b>\n"
            f"• 🔤 Новых слов: <b>{len(vocab_items)}</b>\n"
            f"• ❌ Исправлений ошибок: <b>{len(corrections)}</b>\n"
            f"• ⭐ Закрепленных выражений: <b>{len(good_lang)}</b>\n"
            f"• 💡 Улучшений: <b>{len(suggestions)}</b>\n\n"
            "Карточки сразу добавлены в интервальный алгоритм!"
        )
        await status_msg.edit_text(summary_text, parse_mode="HTML", reply_markup=builder.as_markup())
        
    except Exception as e:
        logger.error(f"Error processing board photo: {e}", exc_info=True)
        safe_error = html.escape(str(e))
        await status_msg.edit_text(f"❌ <b>Произошла ошибка при обработке:</b>\n<code>{safe_error}</code>\nПопробуй скинуть скриншот еще раз.", parse_mode="HTML")

# Category training triggers
@dp.message(F.text == "🚀 Учить карточки")
@dp.message(Command("learn"))
async def learn_all(message: types.Message):
    await send_next_card(message.chat.id, user_id=message.from_user.id, category=None)

@dp.message(F.text == "🔤 Новые слова")
@dp.message(Command("vocab"))
async def learn_vocab(message: types.Message):
    await send_next_card(message.chat.id, user_id=message.from_user.id, category="vocab")

@dp.message(F.text == "❌ Разбор ошибок")
@dp.message(Command("corrections"))
async def learn_corrections(message: types.Message):
    await send_next_card(message.chat.id, user_id=message.from_user.id, category="correction")

@dp.message(F.text == "⭐ Закрепление лексики")
@dp.message(Command("good"))
async def learn_good(message: types.Message):
    await send_next_card(message.chat.id, user_id=message.from_user.id, category="good_language")

@dp.callback_query(F.data == "start_learn_all")
async def cb_start_learn_all(callback: types.CallbackQuery):
    await callback.answer()
    await send_next_card(callback.message.chat.id, user_id=callback.from_user.id, category=None)

async def send_next_card(chat_id: int, user_id: int, category: Optional[str] = None):
    # First look for due cards scoped by user_id
    cards = db.get_due_cards(user_id=user_id, card_type=category, limit=1)
    is_extra_practice = False
    
    if not cards:
        # If no due cards, get any cards for free practice
        cards = db.get_any_cards(user_id=user_id, card_type=category, limit=1)
        is_extra_practice = True
        
    if not cards:
        empty_text = (
            "🎉 <b>На сегодня всё повторено!</b>\n\n"
            "В базе пока нет карточек этой категории или все они уже выучены на сегодня.\n"
            "Скинь новый скриншот доски Miro, чтобы добавить свежий материал!"
        )
        await bot.send_message(chat_id, empty_text, parse_mode="HTML")
        return

    card = cards[0]
    card_id = card["id"]
    USER_SESSIONS.set(user_id, card_id, category)
    
    card_type = card["type"]
    front = html.escape(card["front"])
    transcription = html.escape(card.get("transcription") or "")
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔊 Произношение", callback_data=f"tts_{card_id}")
    builder.button(text="💡 Показать ответ", callback_data=f"show_answer_{card_id}")
    builder.adjust(2)
    
    prefix = "🔄 <i>Повторение вне очереди</i>\n\n" if is_extra_practice else ""
    
    if card_type == "vocab":
        trans_str = f" <code>{transcription}</code>" if transcription else ""
        msg_text = (
            f"{prefix}🔤 <b>СЛОВО ИЗ УРОКА</b>\n\n"
            f"🇬🇧 <b>{front}</b>{trans_str}\n\n"
            "Вспомни перевод и нажми кнопку ниже:"
        )
    elif card_type == "correction":
        msg_text = (
            f"{prefix}❌ <b>РАЗБОР ОШИБКИ</b>\n\n"
            f"❓ {front}\n\n"
            "Подумай, как сказать правильно, и проверь себя:"
        )
    elif card_type == "good_language":
        msg_text = (
            f"{prefix}⭐ <b>ЗАКРЕПЛЕНИЕ ЛЕКСИКИ</b>\n\n"
            f"❓ {front}\n\n"
            "Вспомни точную фразу с урока:"
        )
    else: # suggestion
        msg_text = (
            f"{prefix}💡 <b>LEVEL UP / СИНОНИМ</b>\n\n"
            f"❓ {front}\n\n"
            "Как сказать интереснее и естественнее?"
        )
        
    await bot.send_message(chat_id, msg_text, parse_mode="HTML", reply_markup=builder.as_markup())

@dp.callback_query(F.data.startswith("show_answer_"))
async def cb_show_answer(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        parts = callback.data.split("_")
        if len(parts) < 3:
            await callback.answer("⚠️ Неверный запрос.")
            return
        card_id = int(parts[2])
    except (ValueError, IndexError):
        await callback.answer("⚠️ Некорректный ID карточки.")
        return

    card = db.get_card_by_id(card_id, user_id=user_id)
    if not card:
        await callback.answer("Карточка не найдена.")
        return

    card_type = card["type"]
    front = html.escape(card["front"])
    back = html.escape(card["back"])
    example = html.escape(card.get("example") or "")
    explanation = html.escape(card.get("explanation") or "")
    
    builder = InlineKeyboardBuilder()
    builder.button(text="🔊 Произношение", callback_data=f"tts_{card_id}")
    builder.button(text="🔴 Забыл / Ошибся", callback_data=f"rate_{card_id}_1")
    builder.button(text="🟡 С трудом", callback_data=f"rate_{card_id}_2")
    builder.button(text="🟢 Легко / Знаю", callback_data=f"rate_{card_id}_3")
    builder.adjust(1, 3)
    
    answer_text = ""
    if card_type == "vocab":
        answer_text = (
            f"🔤 <b>{front}</b>\n\n"
            f"🇷🇺 <b>Перевод:</b> {back}\n"
        )
        if example:
            answer_text += f"\n📖 <b>Пример:</b>\n<i>{example}</i>\n"
    elif card_type == "correction":
        answer_text = (
            f"✅ <b>Правильно:</b> <b>{back}</b>\n\n"
        )
        if explanation:
            answer_text += f"💡 <b>Почему так:</b> {explanation}\n\n"
        if example:
            answer_text += f"📝 <b>Разница:</b>\n<i>{example}</i>\n"
    elif card_type == "good_language":
        answer_text = (
            f"⭐ <b>Фраза:</b> <b>{back}</b>\n\n"
        )
        if explanation:
            answer_text += f"🇷🇺 <b>Значение:</b> {explanation}\n\n"
        if example:
            answer_text += f"📖 <b>Пример:</b>\n<i>{example}</i>\n"
    else:
        answer_text = (
            f"💡 <b>Лучше сказать:</b> <b>{back}</b>\n\n"
        )
        if explanation:
            answer_text += f"📝 <b>Контекст:</b> {explanation}\n\n"
            
    answer_text += "\nОцени, насколько хорошо ты это помнишь:"
    await callback.message.edit_text(answer_text, parse_mode="HTML", reply_markup=builder.as_markup())
    await callback.answer()

@dp.callback_query(F.data.startswith("tts_"))
async def cb_play_tts(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        parts = callback.data.split("_")
        if len(parts) < 2:
            await callback.answer("⚠️ Неверный запрос.")
            return
        card_id = int(parts[1])
    except (ValueError, IndexError):
        await callback.answer("⚠️ Некорректный запрос.")
        return

    card = db.get_card_by_id(card_id, user_id=user_id)
    if not card:
        await callback.answer("Карточка не найдена.")
        return
        
    text_to_speak = card.get("pronunciation_text") or card.get("back") or card.get("front")
    await callback.answer("Генерирую озвучку...")
    
    try:
        audio_path = await tts_service.generate_speech(text_to_speak, filename_prefix=f"c_{card_id}")
        safe_caption = html.escape(text_to_speak)
        await bot.send_voice(callback.message.chat.id, voice=FSInputFile(audio_path), caption=f"🗣 <i>{safe_caption}</i>", parse_mode="HTML")
    except Exception as e:
        logger.error(f"TTS error: {e}")
        await callback.message.answer(f"⚠️ Ошибка озвучки: {html.escape(str(e))}", parse_mode="HTML")

@dp.callback_query(F.data.startswith("rate_"))
async def cb_rate_card(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    try:
        parts = callback.data.split("_")
        if len(parts) < 3:
            await callback.answer("⚠️ Неверный запрос.")
            return
        card_id = int(parts[1])
        rating = int(parts[2])
    except (ValueError, IndexError):
        await callback.answer("⚠️ Некорректный рейтинг.")
        return
        
    # Update SRS scoped by user_id
    result = db.update_srs_review(card_id, rating, user_id=user_id)
    
    ratings_map = {1: "🔴 Повторим скоро", 2: "🟡 Запомнено", 3: "🟢 Отлично!"}
    status = ratings_map.get(rating, "Сохранено")
    
    await callback.answer(f"{status} (следующий раз: {result.get('next_review', 'скоро')})")
    
    # Delete old quiz message to keep chat clean
    try:
        await callback.message.delete()
    except Exception:
        pass
        
    # Send next card
    session = USER_SESSIONS.get(user_id)
    category = session.get("category")
    await send_next_card(callback.message.chat.id, user_id=user_id, category=category)

async def main():
    global bot
    if not config.TELEGRAM_BOT_TOKEN:
        print("\n" + "="*60)
        print(" [!] ВНИМАНИЕ: TELEGRAM_BOT_TOKEN не указан!")
        print(" Открой файл .env в папке проекта и вставь токен своего бота:")
        print(f" {config.BASE_DIR / '.env'}")
        print("="*60 + "\n")
        return

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    db.init_db()
    
    if config.ALLOWED_USER_IDS:
        print(f" [🔐] Включен белый список пользователей: {config.ALLOWED_USER_IDS}")
    else:
        print(" [⚠️] ВНИМАНИЕ: ALLOWED_USER_IDS не задан! Бот доступен всем, напиши ему /start чтобы узнать свой ID.")
        
    print("="*60)
    print(" [✓] Бот успешно запущен! Ожидание сообщений и скриншотов...")
    print("="*60)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
