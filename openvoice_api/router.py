from fastapi import APIRouter, UploadFile
from fastapi.responses import FileResponse
import tempfile
from .voice_engine import normalize_audio, convert_voice

router = APIRouter(prefix="/openvoice")

@router.post("/convert")
async def convert(reference: UploadFile, target: UploadFile):
    with tempfile.TemporaryDirectory() as tmpdir:
        ref_path = f"{tmpdir}/ref.wav"
        tgt_path = f"{tmpdir}/tgt.wav"
        out_path = f"{tmpdir}/converted.wav"

        # Save uploads
        with open(ref_path, "wb") as f:
            f.write(await reference.read())
        with open(tgt_path, "wb") as f:
            f.write(await target.read())

        # Normalize both using ffmpeg
        normalize_audio(ref_path, ref_path)
        normalize_audio(tgt_path, tgt_path)

        # Run OpenVoice (placeholder)
        convert_voice(ref_path, tgt_path, out_path)

        return FileResponse(out_path, media_type="audio/wav", filename="converted.wav")
