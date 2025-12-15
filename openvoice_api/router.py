from fastapi import APIRouter, UploadFile, Form
from fastapi.responses import Response, FileResponse
import tempfile
from .voice_engine import text_to_speech, speech_to_text, convert_voice, normalize_audio

router = APIRouter(prefix="/openvoice", tags=["OpenVoice API"])

# 🟣 Text → Speech (OpenAI TTS)
@router.post("/tts")
async def tts(text: str = Form(...)):
    audio_bytes = text_to_speech(text)
    return Response(content=audio_bytes, media_type="audio/mpeg")

# 🟢 Speech → Text (OpenAI Whisper)
@router.post("/stt")
async def stt(file: UploadFile):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name
    result_text = speech_to_text(tmp_path)
    return {"text": result_text}

# 🔵 Voice Conversion (OpenVoice)
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

        # Normalize audio
        normalize_audio(ref_path, ref_path)
        normalize_audio(tgt_path, tgt_path)

        # Placeholder for OpenVoice model
        convert_voice(ref_path, tgt_path, out_path)

        return FileResponse(out_path, media_type="audio/wav", filename="converted.wav")
