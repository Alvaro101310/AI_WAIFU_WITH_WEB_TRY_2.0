# ============================================================
#  face_controller.py — Dual Mode Avatar Controller
#
#  Mode 1 (selalu aktif):
#    Broadcast param ke browser via WebSocket (/face)
#    → Avatar render di browser pakai pixi-live2d-display
#
#  Mode 2 (opsional, aktif kalau VTS_HOST diset):
#    Inject param langsung ke VTube Studio via Cloudflare Tunnel
#    → Kedua mode jalan bersamaan (browser + VTS sync)
# ============================================================

import asyncio
import random

from fastapi import WebSocket
from config import (
    FACE_DEFAULT, PARAM_RANGE, PARAM_ID_MAP,
    SMOOTH_STEPS, SMOOTH_INTERVAL, HOLD_INTERVAL, MOUTH_STEP_INTERVAL,
    VTS_HOST, VTS_PORT, VTS_TOKEN_PATH, VTS_PLUGIN_NAME, VTS_DEVELOPER,
    SKIP_PARAMS,
)


# ============================================================
#  VTS helper — lazy import agar tidak crash kalau pyvts tidak diinstall
# ============================================================

def _try_build_vts():
    """
    Buat instance pyvts kalau VTS_HOST diset.
    Return None kalau VTS_HOST kosong atau pyvts tidak terinstall.
    """
    if not VTS_HOST:
        return None
    try:
        import pyvts
        plugin_info = {
            "plugin_name": VTS_PLUGIN_NAME,
            "developer":   VTS_DEVELOPER,
            "authentication_token_path": VTS_TOKEN_PATH,
        }
        is_remote = VTS_HOST not in ("localhost", "127.0.0.1")
        if is_remote:
            # VTS_HOST contoh: "random-abc.trycloudflare.com"
            return pyvts.vts(
                plugin_info=plugin_info,
                vts_api_info={
                    "version": "1.0",
                    "name": "VTubeStudioPublicAPI",
                    "host": VTS_HOST,
                    "port": 443,
                },
            )
        else:
            return pyvts.vts(plugin_info=plugin_info, port=VTS_PORT)
    except ImportError:
        print("⚠️  pyvts tidak terinstall — VTS mode dimatikan")
        return None
    except Exception as e:
        print(f"⚠️  Gagal init VTS: {e}")
        return None


# ============================================================
#  FaceController
# ============================================================

class FaceController:
    def __init__(self):
        # --- Browser WebSocket clients ---
        self.clients: set[WebSocket] = set()
        self.ws_lock = asyncio.Lock()

        # --- VTS (opsional) ---
        self._vts_instance   = None
        self._vts_connected  = False
        self._vts_lock       = asyncio.Lock()

        # --- State ---
        self.is_speaking     = False
        self.current_values: dict[str, float] = dict(FACE_DEFAULT)
        self.param_range: dict = dict(PARAM_RANGE)

    # ----------------------------------------------------------
    #  Inisialisasi VTS (dipanggil saat startup kalau VTS_HOST ada)
    # ----------------------------------------------------------
    async def try_connect_vts(self):
        """Coba konek ke VTube Studio. Tidak crash kalau gagal."""
        if not VTS_HOST:
            print("ℹ️  VTS_HOST tidak diset — VTS mode off")
            return

        self._vts_instance = _try_build_vts()
        if self._vts_instance is None:
            return

        try:
            print(f"🔌 Konek VTube Studio → wss://{VTS_HOST}")
            await self._vts_instance.connect()
            await self._vts_instance.request_authenticate_token()
            await self._vts_instance.request_authenticate()
            self._vts_connected = True
            print("✅ VTube Studio terhubung!")
        except Exception as e:
            print(f"⚠️  VTS gagal konek: {e} — hanya browser mode")
            self._vts_connected = False

    @property
    def vts_connected(self) -> bool:
        return self._vts_connected

    # ----------------------------------------------------------
    #  Browser WebSocket — register / unregister
    # ----------------------------------------------------------
    async def register(self, ws: WebSocket):
        await ws.accept()
        self.clients.add(ws)
        print(f"🟢 Browser avatar konek (total: {len(self.clients)})")

    def unregister(self, ws: WebSocket):
        self.clients.discard(ws)
        print(f"🔴 Browser avatar disconnect (total: {len(self.clients)})")

    @property
    def browser_connected(self) -> bool:
        return len(self.clients) > 0

    @property
    def any_connected(self) -> bool:
        return self.browser_connected or self._vts_connected

    # ----------------------------------------------------------
    #  Kirim param ke browser (WebSocket)
    # ----------------------------------------------------------
    async def _broadcast_browser(self, params: dict[str, float]):
        """Map internal name → Cubism param ID, kirim ke semua browser."""
        if not self.clients:
            return

        mapped = {}
        for name, value in params.items():
            cubism_id = PARAM_ID_MAP.get(name)
            if cubism_id is None:
                continue
            mapped[cubism_id] = round(value, 4)

        if not mapped:
            return

        payload = {"type": "params", "data": mapped}
        async with self.ws_lock:
            dead = set()
            for ws in self.clients:
                try:
                    await ws.send_json(payload)
                except Exception:
                    dead.add(ws)
            for ws in dead:
                self.clients.discard(ws)

    # ----------------------------------------------------------
    #  Kirim param ke VTube Studio
    # ----------------------------------------------------------
    async def _inject_vts(self, params: dict[str, float]):
        """Inject param batch ke VTube Studio."""
        if not self._vts_connected or self._vts_instance is None:
            return

        batch = [
            {"id": name, "value": round(value, 4), "weight": 1.0}
            for name, value in params.items()
        ]
        if not batch:
            return

        async with self._vts_lock:
            try:
                await self._vts_instance.request({
                    "apiName":    "VTubeStudioPublicAPI",
                    "apiVersion": "1.0",
                    "requestID":  "BatchParam",
                    "messageType":"InjectParameterDataRequest",
                    "data": {"parameterValues": batch},
                })
            except Exception as e:
                print(f"⚠️  VTS inject error: {e}")
                self._vts_connected = False

    # ----------------------------------------------------------
    #  send_batch — kirim ke browser + VTS sekaligus
    # ----------------------------------------------------------
    async def send_batch(self, params: dict[str, float]):
        await asyncio.gather(
            self._broadcast_browser(params),
            self._inject_vts(params),
            return_exceptions=True,
        )

    # ----------------------------------------------------------
    #  Animasi
    # ----------------------------------------------------------
    async def smooth_set(self, targets: dict[str, float]):
        """Smooth lerp ke target values."""
        for _ in range(SMOOTH_STEPS):
            batch = {}
            for param, target in targets.items():
                cur = self.current_values.get(param, 0.0)
                new = cur + (target - cur) * 0.15
                self.current_values[param] = new
                batch[param] = new
            await self.send_batch(batch)
            await asyncio.sleep(SMOOTH_INTERVAL)

        # Snap exact
        batch = {}
        for param, target in targets.items():
            self.current_values[param] = target
            batch[param] = target
        await self.send_batch(batch)

    async def hold_inject(self):
        """Terus inject nilai current selama is_speaking=True."""
        while self.is_speaking:
            batch = {p: v for p, v in self.current_values.items() if p != "MouthOpen"}
            await self.send_batch(batch)
            await asyncio.sleep(HOLD_INTERVAL)

    async def mouth_sync(self):
        """Lip sync buka-tutup mulut."""
        while self.is_speaking:
            target = random.uniform(0.5, 1.0)
            for _ in range(6):
                if not self.is_speaking:
                    break
                self.current_values["MouthOpen"] += (target - self.current_values["MouthOpen"]) * 0.4
                await self.send_batch({"MouthOpen": self.current_values["MouthOpen"]})
                await asyncio.sleep(MOUTH_STEP_INTERVAL)

            for _ in range(6):
                if not self.is_speaking:
                    break
                self.current_values["MouthOpen"] += (0.0 - self.current_values["MouthOpen"]) * 0.4
                await self.send_batch({"MouthOpen": self.current_values["MouthOpen"]})
                await asyncio.sleep(MOUTH_STEP_INTERVAL)

        # Tutup mulut smooth
        for _ in range(10):
            self.current_values["MouthOpen"] *= 0.65
            await self.send_batch({"MouthOpen": self.current_values["MouthOpen"]})
            await asyncio.sleep(MOUTH_STEP_INTERVAL)
        self.current_values["MouthOpen"] = 0.0
        await self.send_batch({"MouthOpen": 0.0})

    async def face_animator(self, targets: dict[str, float]):
        """INTRO → HOLD → OUTRO."""
        full_targets = dict(FACE_DEFAULT)
        full_targets.update(targets)
        full_targets.pop("MouthOpen", None)

        await self.smooth_set(full_targets)
        await self.hold_inject()
        await self.smooth_set({k: v for k, v in FACE_DEFAULT.items() if k != "MouthOpen"})
