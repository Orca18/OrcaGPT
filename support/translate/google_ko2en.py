from googletrans import Translator

def google_bt(text, target_language='en', **kwargs):
    assert isinstance(text, str), "Source input should be string"
    source_language = "ko"
    forward = translator.translate(text, src=source_language, dest=target_language)
    print(forward.text)
    backward = translator.translate(forward.text, src=target_language, dest=source_language)
    print(backward.text)
    return backward.text

translator = Translator()