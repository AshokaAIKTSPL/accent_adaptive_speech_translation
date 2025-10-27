# src/translator.py
from googletrans import Translator

def translate_text(text, target_lang="fr"):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation failed: {e}"
