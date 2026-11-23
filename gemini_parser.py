import base64
import json
import logging
import re
from pathlib import Path
from typing import Dict, Any, List
import httpx

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """
Ты — профессиональный лингвистический ассистент и преподаватель английского языка.
Твоя задача — проанализировать скриншот доски обратной связи (Miro) с урока английского языка и структурировать все элементы для интервального повторения.

На доске есть типовые разделы:
1. "good language" — удачные фразы, которые студент сам употребил на уроке (их нужно закрепить).
2. "corrections" — ошибки студента и правильные варианты (например: "win some time -> buy some time", "have mistakes -> make mistakes").
3. "suggestions" — варианты улучшения речи (например: "sad -> frustrated, upset, disappointed").
4. "new vocab" — новые слова, идиомы и фразы (стикеры с переводом).
5. "pronunciation" — заметки по произношению (если есть).

Верни СТРОГО валидный JSON (без markdown-оберток ```json ... ```) со следующей структурой:
{
  "vocab": [
    {
      "word": "werewolf",
      "translation": "оборотень",
      "transcription": "/ˈwɪəwʊlf/",
      "example": "He turned into a werewolf during the full moon.",
      "raw": "werewolf - оборотень"
    }
  ],
  "corrections": [
    {
      "wrong": "win some time",
      "correct": "buy some time",
      "explanation": "Выиграть время на английском говорят через глагол 'buy' (buy some time), а не 'win'.",
      "quiz": "Исправь ошибку: 'We need to win some time before the deadline.'",
      "pronunciation_text": "buy some time",
      "raw": "win some time -> buy some time"
    }
  ],
  "good_language": [
    {
      "phrase": "set up your server",
      "meaning": "настроить/сконфигурировать сервер",
      "example": "It took me two hours to set up your server properly.",
      "raw": "set up your server"
    }
  ],
  "suggestions": [
    {
      "basic": "sad",
      "advanced": "frustrated, upset, disappointed",
      "explanation": "Вместо банального 'sad', если расстроен из-за срыва планов, лучше сказать 'frustrated' или 'disappointed'.",
      "quiz": "Как сказать более продвинуто: 'I was sad because my code failed'?",
      "pronunciation_text": "frustrated, disappointed",
      "raw": "sad -> frustrated, upset, disappointed"
    }
  ]
}

Если какого-то раздела на фото нет или он пустой, верни для него пустой список [].
Обязательно добавь к новым словам пример использования и транскрипцию.
"""

def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Robustly extracts and parses JSON even if LLM adds conversational text
    or surrounds with ```json ``` markers.
    """
    raw = text.strip()
    
    # Try finding first { and last }
    first_brace = raw.find('{')
    last_brace = raw.rfind('}')
    
    if first_brace != -1 and last_brace != -1 and last_brace > first_brace:
        json_candidate = raw[first_brace:last_brace + 1]
        try:
            parsed = json.loads(json_candidate)
            if isinstance(parsed, dict):
                return sanitize_parsed_schema(parsed)
        except json.JSONDecodeError:
            pass
            
    # Fallback to direct json.loads
    parsed = json.loads(raw)
    if isinstance(parsed, dict):
        return sanitize_parsed_schema(parsed)
    raise ValueError("Extracted payload is not a JSON object")

def sanitize_parsed_schema(data: Any) -> Dict[str, Any]:
    """
    Ensures safe dictionary structure to prevent bot crashes on malformed data.
    """
    if not isinstance(data, dict):
        return {"vocab": [], "corrections": [], "good_language": [], "suggestions": []}
        
    for key in ["vocab", "corrections", "good_language", "suggestions"]:
        items = data.get(key)
        if not isinstance(items, list):
            data[key] = []
        else:
            # Filter only dict items
            data[key] = [item for item in items if isinstance(item, dict)]
            
    return data

async def parse_board_image(image_path: Path, api_key: str) -> Dict[str, Any]:
    """
    Parses Miro board feedback screenshot using Google Gemini Vision API.
    """
    if not api_key:
        raise ValueError("GEMINI_API_KEY не задан в настройках.")

    with open(image_path, "rb") as f:
        image_bytes = f.read()
    image_b64 = base64.b64encode(image_bytes).decode("utf-8")
    
    models_to_try = ["gemini-2.5-flash", "gemini-1.5-flash"]
    last_error = None
    
    async with httpx.AsyncClient(timeout=60.0) as client:
        for model in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
            payload = {
                "contents": [
                    {
                        "parts": [
                            {"text": SYSTEM_PROMPT},
                            {
                                "inline_data": {
                                    "mime_type": "image/png",
                                    "data": image_b64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.2,
                    "response_mime_type": "application/json"
                }
            }
            try:
                response = await client.post(url, json=payload)
                if response.status_code == 200:
                    data = response.json()
                    candidates = data.get("candidates", [])
                    if not candidates:
                        raise RuntimeError("Gemini не вернул ни одного кандидата в ответе")
                        
                    candidate = candidates[0]
                    content = candidate.get("content", {})
                    parts = content.get("parts", [])
                    
                    if not parts or "text" not in parts[0]:
                        finish_reason = candidate.get("finishReason", "UNKNOWN")
                        if finish_reason == "SAFETY":
                            raise RuntimeError("Запрос заблокирован фильтром безопасности Gemini")
                        raise RuntimeError(f"Ответ от Gemini пустой или заблокирован (причина: {finish_reason})")
                        
                    text_content = parts[0]["text"]
                    return extract_json_from_text(text_content)
                else:
                    last_error = f"API error ({model}): {response.status_code} - {response.text}"
                    logger.warning(last_error)
            except Exception as e:
                last_error = str(e)
                logger.error(f"Error calling {model}: {e}")
                
    raise RuntimeError(f"Не удалось распознать изображение через Gemini: {last_error}")

async def translate_word_with_context(word: str, sentence: str = "", api_key: str = "") -> Dict[str, Any]:
    """
    Translates an unfamiliar English word in the context of a sentence using Gemini.
    """
    if not api_key:
        return {
            "word": word,
            "translation": "",
            "transcription": "",
            "explanation": f"Встретилось в примере: «{sentence}»" if sentence else "",
            "example": sentence or f"Example with {word}"
        }

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    prompt = f"""
Ты — словарь английского языка. Переведи слово или фразу "{word}" на русский язык с учетом контекста предложения: "{sentence}".
Верни СТРОГО JSON следующего формата (без markdown-разметки):
{{
  "word": "{word}",
  "translation": "точный русский перевод в данном контексте",
  "transcription": "фонетическая транскрипция в косых чертах, например /ˈwɜːd/",
  "explanation": "краткое пояснение значения или грамматики (1 предложение)",
  "example": "{sentence or f'A simple example sentence with {word}.'}"
}}
"""
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }],
        "generationConfig": {
            "temperature": 0.2,
            "responseMimeType": "application/json"
        }
    }

    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            resp = await client.post(url, json=payload)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates") or []
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        raw_text = parts[0]["text"].strip()
                        match = re.search(r"\{.*\}", raw_text, re.DOTALL)
                        if match:
                            parsed = json.loads(match.group(0))
                            if isinstance(parsed, dict):
                                return {
                                    "word": parsed.get("word") or word,
                                    "translation": parsed.get("translation") or "",
                                    "transcription": parsed.get("transcription") or "",
                                    "explanation": parsed.get("explanation") or "",
                                    "example": parsed.get("example") or sentence
                                }
    except Exception as e:
        logger.warning(f"Gemini word translation failed: {e}")

    return {
        "word": word,
        "translation": "",
        "transcription": "",
        "explanation": f"Из контекста: «{sentence}»" if sentence else "",
        "example": sentence
    }

