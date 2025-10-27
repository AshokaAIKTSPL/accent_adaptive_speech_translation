# src/main.py
from accent_model import detect_accent
from speech_to_text import transcribe_speech
from translator import translate_text
from text_to_speech import speak_text
import os
import sys

def main(audio_file, target_lang="fr"):
    try:
        if not os.path.exists(audio_file):
            print(f"❌ Audio file does not exist: {audio_file}")
            return

        print("🎧 Detecting accent...")
        accent = detect_accent(audio_file)
        print(f"Detected Accent: {accent}")

        print("\n🗣️ Converting speech to text...")
        text = transcribe_speech(audio_file, accent)
        print(f"Recognized Text: {text}")

        if "Error" not in text and text not in ["Could not understand audio", "API unavailable", "Audio file not found"]:
            print("\n🌐 Translating...")
            translated = translate_text(text, target_lang)
            print(f"Translated ({target_lang}): {translated}")

            print("\n🔊 Speaking translated text...")
            speak_text(translated)
        else:
            print("\n❌ Skipping translation and speech due to transcription failure.")

    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Use a raw string for Windows path
    audio_path = r"C:\Users\ashok\accent_adaptive_speech_translation\sample_audio\sample_indian_accent.wav"
    main(audio_path, target_lang="es")  # English → Spanish
