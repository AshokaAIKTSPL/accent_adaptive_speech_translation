# src/accent_model.py
def detect_accent(audio_path):
    """
    Dummy accent detector for demonstration.
    """
    import os
    if not os.path.exists(audio_path):
        print(f"❌ Audio file not found: {audio_path}")
        return "Unknown"
    return "Indian"
