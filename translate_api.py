from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang="es"):
    """Translate text using Google Translate."""
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"
