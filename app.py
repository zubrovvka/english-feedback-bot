import asyncio
import base64
import os
import sys
import uuid
import logging
import socket
from pathlib import Path

# Fix Windows console UTF-8 encoding
if sys.platform == "win32":
    try:
        if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

from flask import Flask, request, jsonify, render_template, send_file
import config
import database as db
import gemini_parser
import tts_service
from services import quiz_service, card_service, translation_service

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 * 1024  # 32MB max upload

# Initialize database on startup
db.init_db()


# -------------------------------------------------------------
# Views & Core Routes
# -------------------------------------------------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/manifest.json")
def manifest():
    return jsonify({
        "name": "English Feedback Trainer",
        "short_name": "EngTrainer",
        "description": "Персональный Active Recall тренажер английского",
        "start_url": "/",
        "display": "standalone",
        "background_color": "#020617",
        "theme_color": "#4f46e5",
        "orientation": "portrait",
        "icons": [
            {
                "src": "data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>🇬🇧</text></svg>",
                "sizes": "192x192 512x512",
                "type": "image/svg+xml",
                "purpose": "any maskable"
            }
        ]
    })


# -------------------------------------------------------------
# Configuration API
# -------------------------------------------------------------

@app.route("/api/config", methods=["GET", "POST"])
def manage_config():
    if request.method == "POST":
        data = request.json or {}
        new_gemini_key = data.get("gemini_api_key", "").strip()
        new_voice = data.get("tts_voice", "").strip()

        env_path = config.BASE_DIR / ".env"
        lines = []
        if env_path.exists():
            with open(env_path, "r", encoding="utf-8") as f:
                lines = f.readlines()

        env_vars = {}
        for line in lines:
            if "=" in line and not line.strip().startswith("#"):
                k, v = line.strip().split("=", 1)
                env_vars[k.strip()] = v.strip()

        if new_gemini_key:
            env_vars["GEMINI_API_KEY"] = new_gemini_key
            config.GEMINI_API_KEY = new_gemini_key

        if new_voice:
            env_vars["TTS_VOICE"] = new_voice
            config.TTS_VOICE = new_voice

        with open(env_path, "w", encoding="utf-8") as f:
            for k, v in env_vars.items():
                f.write(f"{k}={v}\n")

        return jsonify({"success": True, "has_gemini_key": bool(config.GEMINI_API_KEY), "tts_voice": config.TTS_VOICE})

    return jsonify({
        "has_gemini_key": bool(config.GEMINI_API_KEY),
        "tts_voice": config.TTS_VOICE,
        "available_voices": [
            {"id": "en-US-JennyNeural", "name": "Jenny (US, женский)"},
            {"id": "en-US-GuyNeural", "name": "Guy (US, мужской)"},
            {"id": "en-GB-SoniaNeural", "name": "Sonia (UK, женский)"},
            {"id": "en-GB-RyanNeural", "name": "Ryan (UK, мужской)"}
        ]
    })


# -------------------------------------------------------------
# Screenshot OCR Upload API
# -------------------------------------------------------------

@app.route("/api/upload", methods=["POST"])
def upload_screenshot():
    temp_path = config.DATA_DIR / f"temp_{uuid.uuid4().hex}.png"
    try:
        if 'file' in request.files and request.files['file'].filename:
            file = request.files['file']
            file.save(str(temp_path))
        elif request.is_json and 'image_b64' in request.json:
            b64_data = request.json['image_b64']
            if ',' in b64_data:
                b64_data = b64_data.split(',', 1)[1]
            image_bytes = base64.b64decode(b64_data)
            with open(temp_path, "wb") as f:
                f.write(image_bytes)
        else:
            return jsonify({"error": "Файл изображения не передан"}), 400

        if not config.GEMINI_API_KEY:
            return jsonify({"error": "GEMINI_API_KEY не задан. Введи свой бесплатный ключ в Настройках ⚙️"}), 400

        # Parse with Gemini Vision
        parsed_data = asyncio.run(gemini_parser.parse_board_image(temp_path, config.GEMINI_API_KEY))

        # Ingest using card service
        total_added, added_counts = card_service.ingest_parsed_board(parsed_data, user_id=0)

        return jsonify({
            "success": True,
            "total_added": total_added,
            "counts": added_counts,
            "parsed": parsed_data
        })

    except Exception as e:
        logger.error(f"Error processing image: {e}", exc_info=True)
        return jsonify({"error": str(e)}), 500
    finally:
        if temp_path.exists():
            try:
                temp_path.unlink()
            except Exception:
                pass


# -------------------------------------------------------------
# Flashcard Practice & Review APIs
# -------------------------------------------------------------

@app.route("/api/cards/next")
def get_next_card():
    category = request.args.get("category")
    if category in ("", "all", "None", None):
        category = None

    cards = db.get_due_cards(user_id=0, card_type=category, limit=1)
    is_extra = False

    if not cards:
        cards = db.get_any_cards(user_id=0, card_type=category, limit=1)
        is_extra = True

    if not cards:
        return jsonify({"card": None, "is_extra": False})

    card = dict(cards[0])
    if not card.get("translation"):
        trans = translation_service.get_or_create_card_translation(card)
        if trans:
            card["translation"] = trans
    return jsonify({"card": card, "is_extra": is_extra})


@app.route("/api/cards/<int:card_id>/review", methods=["POST"])
def review_card(card_id):
    data = request.json or {}
    rating = data.get("rating")
    if rating not in (1, 2, 3):
        return jsonify({"error": "Рейтинг должен быть 1, 2 или 3"}), 400

    result = db.update_srs_review(card_id, rating, user_id=0)
    return jsonify({"success": True, "srs": result})


# -------------------------------------------------------------
# Active Recall Modes: Cloze Deletion & 4-Choice Quiz
# -------------------------------------------------------------

@app.route("/api/cards/cloze")
def get_cloze_question():
    category = request.args.get("category")
    question = quiz_service.build_cloze_question(user_id=0, category=category)
    if not question:
        return jsonify({"card": None})
    return jsonify(question)


@app.route("/api/cards/quiz")
def get_quiz_question():
    category = request.args.get("category")
    question = quiz_service.build_quiz_question(user_id=0, category=category)
    if not question:
        return jsonify({"error": "Недостаточно карточек для квиза"}), 400
    return jsonify(question)


# -------------------------------------------------------------
# Quick Add Word API
# -------------------------------------------------------------

@app.route("/api/cards/quick-add", methods=["POST"])
def quick_add_word():
    data = request.json or {}
    word = data.get("word", "").strip()
    sentence = data.get("sentence", "").strip()
    translation = data.get("translation", "").strip()
    transcription = data.get("transcription", "").strip()
    explanation = data.get("explanation", "").strip()

    if not word:
        return jsonify({"error": "Слово не указано"}), 400

    # Auto-translate with Gemini if available, or fallback free translation
    if not translation:
        if config.GEMINI_API_KEY:
            try:
                info = asyncio.run(gemini_parser.translate_word_with_context(word, sentence, config.GEMINI_API_KEY))
                translation = info.get("translation") or translation
                transcription = info.get("transcription") or transcription
                explanation = info.get("explanation") or explanation
            except Exception as e:
                logger.warning(f"Auto-translate error: {e}")
        if not translation:
            try:
                translation = translation_service.translate_text(word)
            except Exception as e:
                logger.warning(f"Fallback translation error: {e}")

    card = card_service.create_quick_add_card(
        word=word,
        translation=translation,
        sentence=sentence,
        transcription=transcription,
        explanation=explanation,
        user_id=0
    )
    return jsonify({"success": True, "card": card})


@app.route("/api/translate", methods=["POST"])
def translate_text_endpoint():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"translation": ""})
    translation = translation_service.translate_text(text)
    return jsonify({"translation": translation})


# -------------------------------------------------------------
# Text-To-Speech APIs
# -------------------------------------------------------------

@app.route("/api/tts/<int:card_id>")
def play_card_tts(card_id):
    card = db.get_card_by_id(card_id, user_id=0)
    if not card:
        return jsonify({"error": "Карточка не найдена"}), 404

    text = card.get("pronunciation_text") or card.get("back") or card.get("front")
    try:
        audio_path = asyncio.run(tts_service.generate_speech(text, filename_prefix=f"c_{card_id}"))
        return send_file(str(audio_path), mimetype="audio/mpeg")
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/api/tts/speak", methods=["POST"])
def speak_custom_text():
    data = request.json or {}
    text = data.get("text", "").strip()
    if not text:
        return jsonify({"error": "Пустой текст"}), 400

    try:
        audio_path = asyncio.run(tts_service.generate_speech(text, filename_prefix="quick"))
        return send_file(str(audio_path), mimetype="audio/mpeg")
    except Exception as e:
        logger.error(f"TTS error: {e}")
        return jsonify({"error": str(e)}), 500


# -------------------------------------------------------------
# Cards Database & Statistics APIs
# -------------------------------------------------------------

@app.route("/api/stats")
def get_stats():
    stats = db.get_stats(user_id=0)
    return jsonify(stats)


@app.route("/api/cards", methods=["GET", "POST"])
def list_cards():
    if request.method == "POST":
        data = request.json or {}
        card_id = db.add_card(data, user_id=0)
        return jsonify({"success": True, "card_id": card_id})

    limit = int(request.args.get("limit", 500))
    cards = db.get_all_cards(user_id=0, limit=limit)
    return jsonify({"cards": cards})


@app.route("/api/cards/<int:card_id>", methods=["DELETE"])
def remove_card(card_id):
    success = db.delete_card(card_id, user_id=0)
    return jsonify({"success": success})


# -------------------------------------------------------------
# Network Helper & Server Entry Point
# -------------------------------------------------------------

def get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"


def main():
    port = int(os.environ.get("PORT", 5000))
    local_ip = get_local_ip()
    print("\n" + "="*60)
    print(" [+] English Feedback & ReWord Web-Тренажер запущен!")
    print(f" [*] На компьютере:     http://127.0.0.1:{port}")
    print(f" [*] С телефона (Wi-Fi): http://{local_ip}:{port}")
    print("="*60 + "\n")
    app.run(host="0.0.0.0", port=port, debug=False)


if __name__ == "__main__":
    main()
