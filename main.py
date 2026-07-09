# ============================================================
#  main.py — FastAPI app: chat + avatar dalam 1 page
# ============================================================

import asyncio
import base64
import aiohttp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from config import VTS_HOST
from tts import TTSEngine
from ai_brain import AIBrain, build_system_prompt, parse_tag
from face_controller import FaceController

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

face = FaceController()
brain: AIBrain = None
tts: TTSEngine = None
http_session: aiohttp.ClientSession = None


@app.on_event("startup")
async def startup():
    global brain, tts, http_session

    http_session = aiohttp.ClientSession(
        connector=aiohttp.TCPConnector(limit=10),
        timeout=aiohttp.ClientTimeout(total=15),
    )
    tts = TTSEngine(http_session)

    # Coba konek VTS (opsional, tidak crash kalau gagal)
    await face.try_connect_vts()

    system_prompt = build_system_prompt(face.param_range)
    brain = AIBrain(system_prompt)

    print("🔥 Warming up Gemini...")
    try:
        await brain.warmup()
    except Exception as e:
        print(f"⚠️ Warmup gagal: {e}")
    print("✅ Siap!")


@app.on_event("shutdown")
async def shutdown():
    if http_session:
        await http_session.close()


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "vts_connected": face.vts_connected,
        "browser_connected": face.browser_connected,
    }


@app.get("/", response_class=HTMLResponse)
async def index():
    return FileResponse("static/index.html")


# ----------------------------------------------------------
#  WebSocket /face — broadcast param avatar ke browser
# ----------------------------------------------------------
@app.websocket("/face")
async def ws_face(websocket: WebSocket):
    await face.register(websocket)
    try:
        # Kirim state awal
        await websocket.send_json({
            "type": "params",
            "data": {
                face_controller_map(k): v
                for k, v in face.current_values.items()
            }
        })
        while True:
            # keep-alive, browser tidak perlu kirim apa-apa
            await websocket.receive_text()
    except WebSocketDisconnect:
        face.unregister(websocket)
    except Exception:
        face.unregister(websocket)


def face_controller_map(name):
    from config import PARAM_ID_MAP
    return PARAM_ID_MAP.get(name, name)


# ----------------------------------------------------------
#  WebSocket /chat — chat dengan AI, return teks + audio + trigger animasi
# ----------------------------------------------------------
@app.websocket("/chat")
async def ws_chat(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            user_input = await websocket.receive_text()
            if not user_input.strip():
                continue

            try:
                # 1. Gemini
                full_res = await brain.chat(user_input)

                # 2. Parse tag
                vts_targets, tts_settings, clean_text = parse_tag(full_res, face.param_range)

                # 3. TTS
                audio_bytes = await tts.speak(clean_text, tts_settings)
                audio_b64 = base64.b64encode(audio_bytes).decode() if audio_bytes else None

                # 4. Kirim respons teks + audio ke browser chat
                await websocket.send_json({
                    "type": "reply",
                    "text": clean_text,
                    "audio_b64": audio_b64,
                })

                # 5. Jalankan animasi (broadcast ke /face + VTS kalau aktif)
                if audio_bytes:
                    asyncio.create_task(run_with_speaking(vts_targets, estimate_duration(clean_text)))

            except Exception as e:
                await websocket.send_json({"type": "error", "message": str(e)})

    except WebSocketDisconnect:
        pass


def estimate_duration(text: str) -> float:
    """Estimasi durasi audio dari panjang teks (~14 char/detik untuk TTS ID)."""
    return max(1.0, len(text) / 14.0)


async def run_with_speaking(vts_targets: dict, duration: float):
    """
    Set is_speaking=True selama estimasi durasi audio,
    jalankan mouth_sync + face_animator bersamaan.
    """
    face.is_speaking = True

    sync_task = asyncio.create_task(face.mouth_sync())
    anim_task = asyncio.create_task(face.face_animator(vts_targets))

    await asyncio.sleep(duration)
    face.is_speaking = False

    await sync_task
    await anim_task
