import subprocess
import os
from pathlib import Path

# Example: normalize audio and prepare it for OpenVoice
def normalize_audio(input_path: str, output_path: str):
    """Uses ffmpeg to ensure WAV 16kHz mono format."""
    command = [
        "ffmpeg",
        "-y",  # overwrite
        "-i", input_path,
        "-ac", "1",  # mono
        "-ar", "16000",  # 16k sample rate
        output_path
    ]
    subprocess.run(command, check=True)
    return output_path

# Placeholder for your OpenVoice inference
def convert_voice(reference_audio: str, target_audio: str, output_path: str):
    """
    Run OpenVoice inference (to be filled with your actual logic).
    For now, it just copies target_audio → output_path.
    """
    Path(output_path).write_bytes(Path(target_audio).read_bytes())
    return output_path
