# ============================================================
#  tts.py — Text-to-Speech engine (ElevenLabs)
#  Mau ganti TTS? Edit file ini aja, main.py tidak perlu diubah.
# ============================================================

import aiohttp
import asyncio
from config import (
    ELEVENLABS_API_KEY, VOICE_ID,
    TTS_MODEL, TTS_STABILITY, TTS_SIMILARITY
)


class TTSEngine:
    def __init__(self, session: aiohttp.ClientSession):
        self.session = session

    async def speak(self, text: str, tts_settings: dict = None) -> bytes | None:
        """
        Convert teks ke audio bytes (mp3).
        tts_settings: dict opsional dari AI → {"stability": x, "style": y}
        Kalau None, pakai default dari config / Railway env vars.
        """
        stability = tts_settings.get("stability", TTS_STABILITY) if tts_settings else TTS_STABILITY
        style     = tts_settings.get("style", 0.0) if tts_settings else 0.0

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"
        headers = {
            "xi-api-key":   ELEVENLABS_API_KEY,
            "Content-Type": "application/json",
        }
        payload = {
            "text":     text,
            "model_id": TTS_MODEL,
            "voice_settings": {
                "stability":        round(stability, 2),
                "similarity_boost": TTS_SIMILARITY,
                "style":            round(style, 2),
            },
        }
        try:
            async with self.session.post(url, json=payload, headers=headers) as res:
                if res.status == 200:
                    return await res.read()
                body = await res.text()
                print(f"❌ TTS Error ({res.status}): {body}")
                return None
        except asyncio.TimeoutError:
            print("❌ TTS timeout!")
            return None
        except Exception as e:
            print(f"❌ TTS gagal: {e}")
            return None
