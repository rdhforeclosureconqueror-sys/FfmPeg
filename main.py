from fastapi import FastAPI
import shutil
import subprocess

# Import the OpenVoice router
try:
    from openvoice_api.router import router as openvoice_router
except ImportError:
    openvoice_router = None

app = FastAPI(
    title="OpenVoice + OpenAI Voice Gateway",
    description="Unified voice API for STT, TTS, and OpenVoice processing",
    version="1.0.0"
)

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI + FFmpeg + OpenVoice ready"}

@app.head("/")
def root_head():
    # Prevent 405 spam from Render
    return

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/ffmpeg")
def ffmpeg_check():
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        return {"ffmpeg_found": False, "path": None}
    version_line = subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0]
    return {"ffmpeg_found": True, "path": ffmpeg_path, "version_line": version_line}

# Attach OpenVoice router
if openvoice_router:
    app.include_router(openvoice_router)
