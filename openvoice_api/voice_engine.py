import openai
import os
import subprocess
from pathlib import Path

openai.api_key = os.getenv("OPENAI_API_KEY")

# 🎤 --- TEXT → SPEECH (TTS) ---
def text_to_speech(text: str):
    """Convert text to spoken audio using OpenAI's TTS model."""
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=text
    )
    return response.read()


# 🧠 --- SPEECH → TEXT (STT) ---
def speech_to_text(audio_path: str):
    """Transcribe speech to text using OpenAI Whisper."""
    with open(audio_path, "rb") as f:
        result = openai.audio.transcriptions.create(
            model="whisper-1",
            file=f
        )
    return result.text


# 🧬 --- VOICE CONVERSION (OpenVoice Placeholder) ---
def convert_voice(reference_audio: str, target_audio: str, output_path: str):
    """
    Placeholder function for OpenVoice inference.
    Replace this with your model's inference code later.
    """
    Path(output_path).write_bytes(Path(target_audio).read_bytes())
    return output_path


# 🎛️ --- AUDIO NORMALIZATION (FFmpeg) ---
def normalize_audio(input_path: str, output_path: str):
    """Normalize input audio to 16kHz mono WAV using FFmpeg."""
    cmd = [
        "ffmpeg", "-y",
        "-i", input_path,
        "-ac", "1",
        "-ar", "16000",
        output_path
    ]
    subprocess.run(cmd, check=True)
    return output_path
