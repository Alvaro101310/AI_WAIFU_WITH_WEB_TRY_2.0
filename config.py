# ============================================================
#  config.py — Semua setting via Railway Environment Variables
#
#  Cara edit: Railway Dashboard → Project → Service → Variables
#  Setelah save, Railway auto-restart. Tidak perlu redeploy.
#
#  WAJIB diset di Railway:
#    GEMINI_API_KEY
#    ELEVENLABS_API_KEY
#
#  Sisanya sudah punya default, opsional diubah.
# ============================================================

import os

# ============================================================
#  API KEYS (wajib)
# ============================================================
GEMINI_API_KEY     = os.environ.get("GEMINI_API_KEY", "")
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY", "")
VOICE_ID           = os.environ.get("VOICE_ID", "hpp4J3VqNfWAUOO0d1Us")

# ============================================================
#  GEMINI — Model & Behavior
#
#  GEMINI_MODEL options:
#    gemini-2.5-flash-lite  ← default, paling cepat & murah
#    gemini-2.5-flash       ← lebih pintar, sedikit lebih lambat
#    gemini-2.5-pro         ← paling pintar, paling lambat
#    gemini-2.0-flash       ← alternatif cepat
#
#  MAX_HISTORY: jumlah pesan yang diingat (2 = 1 tanya-jawab)
# ============================================================
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")
MAX_HISTORY  = int(os.environ.get("MAX_HISTORY", "10"))

# ============================================================
#  TTS — ElevenLabs
#
#  TTS_MODEL options:
#    eleven_multilingual_v2  ← default, terbaik untuk bahasa Indonesia
#    eleven_turbo_v2_5       ← lebih cepat, sedikit kurang natural
#    eleven_turbo_v2         ← paling cepat
#
#  TTS_STABILITY  : 0.0~1.0 (default 0.4) — kestabilan suara
#  TTS_SIMILARITY : 0.0~1.0 (default 0.8) — kemiripan voice clone
# ============================================================
TTS_MODEL      = os.environ.get("TTS_MODEL", "eleven_multilingual_v2")
TTS_STABILITY  = float(os.environ.get("TTS_STABILITY", "0.4"))
TTS_SIMILARITY = float(os.environ.get("TTS_SIMILARITY", "0.8"))

# ============================================================
#  KARAKTER — Identitas & Kepribadian AI
#
#  KARAKTER_NAMA          : nama karakter (default: Aoi)
#  KARAKTER_CREATOR       : nama creator / user utama (default: Jonathan)
#  KARAKTER_DESKRIPSI     : deskripsi kepribadian singkat
#  KARAKTER_GAYA_NGOMONG  : instruksi gaya bicara
#  KARAKTER_RESPONSE_LEN  : panjang jawaban dalam kata (default: "8-12")
# ============================================================
KARAKTER = {
    "nama":    os.environ.get("KARAKTER_NAMA", "Aoi"),
    "creator": os.environ.get("KARAKTER_CREATOR", "Jonathan"),
    "deskripsi": os.environ.get(
        "KARAKTER_DESKRIPSI",
        "cewek yang lembut, manis, dan perhatian. Natural dan hangat — bukan robot."
    ),
    "gaya_ngomong": os.environ.get(
        "KARAKTER_GAYA_NGOMONG",
        "Santai dan natural kayak ngobrol sama orang yang udah kenal lama. "
        "Jangan pakai kalimat template atau basa-basi. Ekspresif secukupnya, bukan lebay. "
        "Bukan karakter tsundere — gak perlu jual mahal atau galak-galak manja. "
        "Ngomong kayak manusia beneran, bukan kayak karakter anime yang teriak-teriak."
    ),
    "response_len": os.environ.get("KARAKTER_RESPONSE_LEN", "8-12"),
}

# ============================================================
#  ANIMASI — Timing & Smoothing
#
#  SMOOTH_STEPS    : jumlah langkah lerp (default: 30)
#  SMOOTH_INTERVAL : delay tiap step lerp dalam detik (default: 0.02)
#  HOLD_INTERVAL   : interval inject saat hold (default: 0.03)
#  MOUTH_INTERVAL  : interval lip sync step (default: 0.03)
# ============================================================
SMOOTH_STEPS        = int(os.environ.get("SMOOTH_STEPS", "30"))
SMOOTH_INTERVAL     = float(os.environ.get("SMOOTH_INTERVAL", "0.02"))
HOLD_INTERVAL       = float(os.environ.get("HOLD_INTERVAL", "0.03"))
MOUTH_STEP_INTERVAL = float(os.environ.get("MOUTH_STEP_INTERVAL", "0.03"))

# ============================================================
#  VTS (VTube Studio) — OPSIONAL
#
#  Kalau VTS_HOST diset, sistem otomatis juga inject ke VTube Studio
#  via Cloudflare Tunnel, SEKALIGUS tetap broadcast ke browser.
#
#  VTS_HOST : hostname tunnel, misal: random-abc.trycloudflare.com
#             (kosong = VTS dimatikan, hanya browser render)
#  VTS_PORT : port VTS lokal (default 8001, biasanya tidak perlu diubah)
# ============================================================
VTS_HOST         = os.environ.get("VTS_HOST", "")
VTS_PORT         = int(os.environ.get("VTS_PORT", "8001"))
VTS_TOKEN_PATH   = "./vts_token.txt"
VTS_PLUGIN_NAME  = os.environ.get("VTS_PLUGIN_NAME", "AI_Waifu_Aoi")
VTS_DEVELOPER    = os.environ.get("VTS_DEVELOPER", "Jonathan")

# ============================================================
#  FACE PARAMS — Nilai Default & Range
# ============================================================

FACE_DEFAULT = {
    "MouthOpen":    0.0,
    "MouthSmile":   0.0,
    "CheekPuff":    0.0,
    "FaceAngry":    0.0,
    "Brows":        0.0,
    "Tears":        0.0,
    "HeartEyes":    0.0,
    "EyeRoll":      0.0,
    "EyeSmile":     0.0,
    "Drool":        0.0,
    "DarkAura":     0.0,
    "HeartHands":   0.0,
    "PeaceSign":    0.0,
    "EyeOpenLeft":  1.0,
    "EyeOpenRight": 1.0,
    "EyeLeftX":     0.0,
    "EyeLeftY":     0.0,
    "EyeRightX":    0.0,
    "EyeRightY":    0.0,
    "TongueOut":    0.0,
    "FaceAngleX":   0.0,
    "FaceAngleY":   0.0,
    "FaceAngleZ":   0.0,
}

PARAM_RANGE = {
    "MouthOpen":    (0.0, 1.0),
    "MouthSmile":   (-1.0, 1.0),
    "CheekPuff":    (0.0, 1.0),
    "FaceAngry":    (0.0, 1.0),
    "Brows":        (-1.0, 1.0),
    "Tears":        (0.0, 1.0),
    "HeartEyes":    (0.0, 1.0),
    "EyeRoll":      (0.0, 1.0),
    "EyeSmile":     (0.0, 1.0),
    "Drool":        (0.0, 1.0),
    "DarkAura":     (0.0, 1.0),
    "HeartHands":   (0.0, 1.0),
    "PeaceSign":    (0.0, 1.0),
    "EyeOpenLeft":  (0.0, 1.0),
    "EyeOpenRight": (0.0, 1.0),
    "EyeLeftX":     (-1.0, 1.0),
    "EyeLeftY":     (-1.0, 1.0),
    "EyeRightX":    (-1.0, 1.0),
    "EyeRightY":    (-1.0, 1.0),
    "TongueOut":    (0.0, 1.0),
    "FaceAngleX":   (-30.0, 30.0),
    "FaceAngleY":   (-30.0, 30.0),
    "FaceAngleZ":   (-30.0, 30.0),
}

# ============================================================
#  PARAM_ID_MAP — mapping internal name → Cubism param ID
#
#  Sesuaikan value dengan param ID di file .model3.json kamu.
#  Set None kalau model tidak punya param tersebut.
#
#  Override via env var: PARAM_MAP_MouthOpen=ParamMouthOpenY
#  (prefix PARAM_MAP_ + nama internal)
# ============================================================
_default_param_map = {
    # Param IDs dari 晴霓Live2D.cdi3.json (model baru)
    "MouthOpen":    "ParamMouthOpenY",   # 嘴 张开和闭合 — buka mulut (lip sync)
    "MouthSmile":   "ParamMouthForm",    # 嘴 变形 — bentuk mulut (-1=cemberut, 1=senyum)
    "CheekPuff":    "LianHong",          # 脸红 — pipi merah/blush
    "FaceAngry":    "ShengQi",           # 生气 — ekspresi marah
    "Brows":        "ParamBrowLForm",    # 左眉 変形 — alis (satu param, gerakin dua alis)
    "Tears":        "LiuLei",            # 流泪 — nangis/berlinang air mata
    "HeartEyes":    "AXY",               # 爱心眼 — mata love/kagum
    "EyeRoll":      "BVS2",              # 翻白眼 — eyeroll (males/eneg)
    "EyeSmile":     "ParamEyeLSmile",    # 左眼 微笑 — mata senyum melengkung
    "Drool":        "KouShui",           # 口水 — ngiler (lucu/pengen/melongo)
    "DarkAura":     "LianHei",           # 脸黑 — aura gelap (syok/eneg banget/dead inside)
    "HeartHands":   "BXS",               # 比心手 — gestur tangan bentuk hati
    "PeaceSign":    "BVS",               # 比V手 — gestur tangan V/peace
    "EyeOpenLeft":  "ParamEyeLOpen",     # 左眼 开闭 — buka mata kiri
    "EyeOpenRight": "ParamEyeROpen",     # 右眼 开闭 — buka mata kanan
    "EyeLeftX":     "ParamEyeBallX",     # 眼珠 X — arah bola mata X
    "EyeLeftY":     "ParamEyeBallY",     # 眼珠 Y — arah bola mata Y
    "EyeRightX":    "ParamEyeBallX",     # share 1 param utk kedua mata
    "EyeRightY":    "ParamEyeBallY",
    "TongueOut":    "TuShe",             # 吐舌 — lidah keluar
    "FaceAngleX":   "ParamAngleX",       # 角度 X — rotasi kepala kiri/kanan
    "FaceAngleY":   "ParamAngleY",       # 角度 Y — rotasi kepala atas/bawah
    "FaceAngleZ":   "ParamAngleZ",       # 角度 Z — kemiringan kepala
}

# Cek env var override untuk tiap param
PARAM_ID_MAP = {}
for _k, _v in _default_param_map.items():
    _env_key = f"PARAM_MAP_{_k}"
    _override = os.environ.get(_env_key)
    if _override is not None:
        PARAM_ID_MAP[_k] = _override if _override.upper() != "NONE" else None
    else:
        PARAM_ID_MAP[_k] = _v

# ============================================================
#  PARAM GUIDES — untuk prompt AI (tidak perlu diubah)
# ============================================================

SKIP_PARAMS = {"MouthOpen"}

PARAM_GUIDE = {
    "FaceAngleX":   "rotasi kiri/kanan (-=lihat kiri, +=lihat kanan)",
    "FaceAngleY":   "rotasi atas/bawah (-=nunduk, +=ngangkat kepala)",
    "FaceAngleZ":   "miring kepala (-=condong kiri, +=condong kanan)",
    "EyeLeftX":     "arah pupil kiri (-=kiri, +=kanan)",
    "EyeLeftY":     "arah pupil kiri (-=bawah, +=atas)",
    "EyeRightX":    "arah pupil kanan (-=kiri, +=kanan)",
    "EyeRightY":    "arah pupil kanan (-=bawah, +=atas)",
    "EyeOpenLeft":  "mata kiri (0=nutup, 1=buka)",
    "EyeOpenRight": "mata kanan (0=nutup, 1=buka)",
    "EyeSmile":     "mata senyum melengkung ala bulan sabit (0=normal, 1=penuh) — senyum tulus/senang banget",
    "MouthSmile":   "senyum (-1=cemberut, 0=datar, 1=senyum lebar)",
    "CheekPuff":    "pipi merah/blush (0=normal, 1=merah penuh) — buat malu/senang",
    "FaceAngry":    "ekspresi marah (0=normal, 1=marah penuh)",
    "Brows":        "alis (-1=turun/kesel, 0=normal, 1=naik/kaget)",
    "TongueOut":    "lidah (0=masuk, 1=keluar) — becanda/meledek",
    "Tears":        "berlinang air mata (0=kering, 1=nangis penuh) — sedih/terharu",
    "HeartEyes":    "mata love (0=normal, 1=love penuh) — kagum/naksir/gemas",
    "EyeRoll":      "eyeroll/mata melirik ke atas (0=normal, 1=penuh) — males/eneg/sarkas",
    "Drool":        "ngiler (0=normal, 1=penuh) — lucu/pengen sesuatu/melongo kaget",
    "DarkAura":     "aura wajah gelap (0=normal, 1=penuh) — syok berat/eneg banget/dead inside, kesan komikal",
    "HeartHands":   "gestur tangan bentuk hati (0=turun, 1=penuh) — sayang/gemas/nunjukin cinta",
    "PeaceSign":    "gestur tangan V/peace (0=turun, 1=penuh) — senang/becanda/pamer semangat",
}

TTS_PARAM_GUIDE = {
    "stability": "0.0~1.0 — kestabilan suara (0.0=sangat ekspresif, 1.0=sangat stabil/datar)",
    "style":     "0.0~1.0 — intensitas gaya bicara (0.0=netral/flat, 1.0=sangat ekspresif)",
}

EMOSI_TTS_GUIDE = """
Referensi TTS per emosi (AI bebas menyesuaikan):
  Senang/gembira    → stability=0.3, style=0.8
  Malu/kikuk        → stability=0.4, style=0.5
  Marah/kesal       → stability=0.7, style=0.9
  Sedih/murung      → stability=0.8, style=0.2
  Tsundere/cuek     → stability=0.5, style=0.4
  Netral/santai     → stability=0.4, style=0.3
  Kaget/terkejut    → stability=0.2, style=0.9
"""