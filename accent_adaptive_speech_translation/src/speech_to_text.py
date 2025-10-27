# src/speech_to_text.py
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import sys
import shutil
import zipfile
import urllib.request

FFMPEG_DIR = r"C:\ffmpeg"

def download_ffmpeg():
    """Download ffmpeg if not installed."""
    print("📥 ffmpeg not found. Downloading ffmpeg...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(tempfile.gettempdir(), "ffmpeg.zip")

    urllib.request.urlretrieve(url, zip_path)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(tempfile.gettempdir())

    # Move extracted folder to C:\ffmpeg
    extracted_folder = [f for f in os.listdir(tempfile.gettempdir()) if f.startswith("ffmpeg")][0]
    extracted_path = os.path.join(tempfile.gettempdir(), extracted_folder)
    if os.path.exists(FFMPEG_DIR):
        shutil.rmtree(FFMPEG_DIR)
    shutil.move(extracted_path, FFMPEG_DIR)
    print(f"✅ ffmpeg downloaded to {FFMPEG_DIR}")

def find_ffmpeg():
    """
    Locate ffmpeg and ffprobe executables.
    Downloads automatically if missing.
    """
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")

    if not ffmpeg_path or not ffprobe_path:
        # Check default folder
        ffmpeg_path = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")
        ffprobe_path = os.path.join(FFMPEG_DIR, "bin", "ffprobe.exe")
        if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
            download_ffmpeg()

    # Final paths
    ffmpeg_path = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")
    ffprobe_path = os.path.join(FFMPEG_DIR, "bin", "ffprobe.exe")
    if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
        raise FileNotFoundError("ffmpeg or ffprobe not found after download!")
    return ffmpeg_path, ffprobe_path

def transcribe_speech(audio_path, accent="neutral"):
    if not os.path.exists(audio_path):
        return "Audio file not found"

    recognizer = sr.Recognizer()
    try:
        # Ensure ffmpeg is ready
        ffmpeg_path, ffprobe_path = find_ffmpeg()
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffprobe = ffprobe_path

        audio_data = AudioSegment.from_file(audio_path)
        audio_data = audio_data.set_channels(1).set_frame_rate(16000)

        with tempfile.NamedTemporaryFile(suffix=".wav") as tmpfile:
            audio_data.export(tmpfile.name, format="wav")
            with sr.AudioFile(tmpfile.name) as source:
                audio = recognizer.record(source)

            lang_map = {
                "indian": "en-IN",
                "british": "en-GB",
                "american": "en-US"
            }
            lang = lang_map.get(accent.lower(), "en-US")
            text = recognizer.recognize_google(audio, language=lang)
            return text

    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "API unavailable"
    except Exception as e:
        return f"Error: {e}"
# src/speech_to_text.py
import speech_recognition as sr
from pydub import AudioSegment
import tempfile
import os
import shutil
import zipfile
import urllib.request

FFMPEG_DIR = r"C:\ffmpeg"

def download_ffmpeg():
    """Download ffmpeg if not installed."""
    print("📥 ffmpeg not found. Downloading ffmpeg...")
    url = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    zip_path = os.path.join(tempfile.gettempdir(), "ffmpeg.zip")

    # Download the zip file
    urllib.request.urlretrieve(url, zip_path)

    # Extract the zip
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(tempfile.gettempdir())

    # Find the extracted folder
    extracted_folder = next(
        (f for f in os.listdir(tempfile.gettempdir()) if f.lower().startswith("ffmpeg")), None
    )
    if not extracted_folder:
        raise FileNotFoundError("Failed to find extracted ffmpeg folder.")

    extracted_path = os.path.join(tempfile.gettempdir(), extracted_folder)

    # Remove old ffmpeg folder if exists
    if os.path.exists(FFMPEG_DIR):
        shutil.rmtree(FFMPEG_DIR)

    # Move the folder to C:\ffmpeg
    shutil.move(extracted_path, FFMPEG_DIR)
    print(f"✅ ffmpeg downloaded to {FFMPEG_DIR}")

def find_ffmpeg():
    """
    Locate ffmpeg and ffprobe executables.
    Downloads automatically if missing.
    """
    ffmpeg_path = shutil.which("ffmpeg")
    ffprobe_path = shutil.which("ffprobe")

    # Check default folder
    if not ffmpeg_path or not ffprobe_path:
        ffmpeg_path = os.path.join(FFMPEG_DIR, "bin", "ffmpeg.exe")
        ffprobe_path = os.path.join(FFMPEG_DIR, "bin", "ffprobe.exe")
        if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
            download_ffmpeg()

    # Final verification
    if not os.path.exists(ffmpeg_path) or not os.path.exists(ffprobe_path):
        raise FileNotFoundError("ffmpeg or ffprobe not found after download!")

    return ffmpeg_path, ffprobe_path

def transcribe_speech(audio_path, accent="neutral"):
    """
    Convert speech to text with accent-aware recognition.
    """
    if not os.path.exists(audio_path):
        return "Audio file not found"

    recognizer = sr.Recognizer()
    try:
        # Ensure ffmpeg is ready
        ffmpeg_path, ffprobe_path = find_ffmpeg()
        AudioSegment.converter = ffmpeg_path
        AudioSegment.ffprobe = ffprobe_path

        # Load and preprocess audio
        audio_data = AudioSegment.from_file(audio_path)
        audio_data = audio_data.set_channels(1).set_frame_rate(16000)

        # Export to temporary WAV for recognition
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmpfile:
            audio_data.export(tmpfile.name, format="wav")
            tmpfile_path = tmpfile.name

        with sr.AudioFile(tmpfile_path) as source:
            audio = recognizer.record(source)

        # Remove temporary file
        os.remove(tmpfile_path)

        # Accent-aware language mapping
        lang_map = {
            "indian": "en-IN",
            "british": "en-GB",
            "american": "en-US"
        }
        lang = lang_map.get(accent.lower(), "en-US")

        text = recognizer.recognize_google(audio, language=lang)
        return text

    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError:
        return "API unavailable"
    except Exception as e:
        return f"Error: {e}"
