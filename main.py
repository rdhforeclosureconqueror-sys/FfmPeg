from fastapi import FastAPI
import shutil
import subprocess

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/ffmpeg")
def ffmpeg_check():
    ffmpeg_path = shutil.which("ffmpeg")
    if not ffmpeg_path:
        return {"ffmpeg_found": False, "path": None}

    # Get version (safe + useful)
    out = subprocess.check_output(["ffmpeg", "-version"], text=True).splitlines()[0]
    return {"ffmpeg_found": True, "path": ffmpeg_path, "version_line": out}
