from deep_translator import GoogleTranslator

def translate_to_greek(text):
    """
    Translates English text into Greek using Google Translate.
    :param text: English text to translate.
    :return: Greek translation.
    """
    translator = GoogleTranslator(source="en", target="el")
    return translator.translate(text)