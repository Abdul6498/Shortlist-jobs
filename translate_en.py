from googletrans import Translator


def translate_to_eng(text):
    # init the Google API translator
    translator = Translator()

    # translate a spanish text to english text (by default)
    translation = translator.translate(text)
    # print(f"{translation.origin} ({translation.src}) --> {translation.text} ({translation.dest})")

    return translation

