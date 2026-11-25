import hashlib
import re
from pathlib import Path
import edge_tts
import config

MAX_TEXT_LENGTH = 500


async def generate_speech(text: str, filename_prefix: str = "card") -> Path:
    """
    Generates high quality neural pronunciation audio using Microsoft Edge TTS.
    Returns path to the generated mp3 file.
    Hardened against:
    - Empty / whitespace-only inputs
    - Path traversal in filename_prefix
    - Hash collision by using full 256-bit SHA256
    - Resource exhaustion by capping text length
    """
    clean_text = text.strip()
    if not clean_text:
        raise ValueError("Text for speech generation cannot be empty")
        
    if len(clean_text) > MAX_TEXT_LENGTH:
        clean_text = clean_text[:MAX_TEXT_LENGTH]

    # Sanitize prefix to prevent directory traversal
    safe_prefix = re.sub(r'[^a-zA-Z0-9_-]', '', filename_prefix) or "audio"

    # Read voice dynamically so settings changes apply immediately without restart
    voice = getattr(config, "TTS_VOICE", "en-US-JennyNeural") or "en-US-JennyNeural"

    # 256-bit SHA-256 including voice so switching voices regenerates audio
    text_hash = hashlib.sha256(f"{voice}:{clean_text}".encode('utf-8')).hexdigest()

    audio_dir = config.AUDIO_DIR
    out_path = audio_dir / f"{safe_prefix}_{text_hash}.mp3"

    # Ensure resolved path remains strictly within AUDIO_DIR
    resolved_out = out_path.resolve()
    resolved_audio_dir = audio_dir.resolve()
    if resolved_audio_dir not in resolved_out.parents:
        raise ValueError("Security violation: path traversal detected")

    if out_path.exists() and out_path.stat().st_size > 0:
        return out_path

    communicate = edge_tts.Communicate(clean_text, voice=voice)
    await communicate.save(str(out_path))
    
    if not out_path.exists() or out_path.stat().st_size == 0:
        if out_path.exists():
            out_path.unlink(missing_ok=True)
        raise RuntimeError("Speech generation produced an empty audio file")
        
    return out_path
