# src/text_to_speech.py
import pyttsx3

def speak_text(text, lang="en"):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')

    for voice in voices:
        lang_code = voice.languages[0]
        if isinstance(lang_code, bytes):
            lang_code = lang_code.decode('utf-8')
        if 'en' in lang_code:
            engine.setProperty('voice', voice.id)
            break

    engine.say(text)
    engine.runAndWait()
