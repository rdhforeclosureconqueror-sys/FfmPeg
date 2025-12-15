from fastapi import FastAPI
import shutil
import subprocess

# Import the new OpenVoice router (we’ll add this next)
try:
    from openvoice_api.router import router as openvoice_router
except ImportError:
    openvoice_router = None

app = FastAPI(
    title="OpenVoice + FFmpeg API",
    description="Unified voice processing API powered by FastAPI and OpenVoice",
    version="1.0.0"
)

# --- Base health + ffmpeg endpoints (keep these) ---
@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is live. Try /docs or /ffmpeg"}

@app.head("/")
def root_head():
    # Prevent 405 spam from Render health checks
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

# --- OpenVoice endpoints (mounted dynamically) ---
if openvoice_router:
    app.include_router(openvoice_router)
