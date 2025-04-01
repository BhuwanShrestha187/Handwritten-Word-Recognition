'''
    Filename: translate_api.py
    Author: Bhuwan Shrestha, Alen Varghese, Shubh Soni, and Dev Patel
    Date: 2025-04-01
    Project: Handwritten OCR | Capstone Project 2025
    Course: Systems Project
    Description: This is the translate API for the Handwritten OCR project.
'''


'''
    References: We have used the Google Translate API to translate the text. The API is free to use and has a limit of 1000 requests per user. 
    The link to the API is given below: 
    - https://github.com/googletrans/googletrans
    - https://github.com/google/translate-python
'''
from googletrans import Translator

translator = Translator()

def translate_text(text, target_lang="es"):
    """Translate text using Google Translate."""
    try:
        translated = translator.translate(text, dest=target_lang)
        return translated.text
    except Exception as e:
        return f"Translation Error: {str(e)}"
