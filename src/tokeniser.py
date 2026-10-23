import spacy
from spacy.lang.char_classes import ALPHA, PUNCT
from spacy.util import compile_infix_regex

def build_yoruba_tokeniser(nlp):
    """
    Configures a blank spaCy pipeline to respect Yorùbá diacritics,
    underdot vowels, and apostrophe-based elision.
    """
    # Include Yorùbá characters in alphabetic classes
    yoruba_chars = "a-zA-Záàéèẹ́ẹ̀íìóòọ́ọ̀úùṣÁÀÉÈẸ́Ẹ̀ÍÌÓÒỌ́Ọ̀ÚÙṢ"
    custom_alpha = f"{ALPHA}|[{yoruba_chars}]"
    
    # Treat apostrophe within words as elision, not a token split
    infixes = [
        r"(?<=[{a}])['’](?=[{a}])".format(a=custom_alpha),
        r"(?<=[{a}])([/])(?=[{a}])".format(a=custom_alpha),
    ] + [r"(?<=[0-9])-(?=[0-9])"]
    
    infix_re = compile_infix_regex(tuple(infixes))
    nlp.tokenizer.infix_finditer = infix_re.finditer
    return nlp

def create_yoruba_pipeline():
    """Builds and returns the blank Yorùbá NLP pipeline."""
    nlp = spacy.blank("yo")
    return build_yoruba_tokeniser(nlp)