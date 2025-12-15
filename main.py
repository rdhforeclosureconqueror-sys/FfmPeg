from fastapi import FastAPI
import shutil
import subprocess

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "FastAPI is live. Try /docs or /ffmpeg"}

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
