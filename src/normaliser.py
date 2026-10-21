import unicodedata
import re

def normalise_yoruba_text(text: str) -> str:
    """
    Standardises Yorùbá text to Unicode Canonical Composition (NFC).
    Ensures vowels with tone marks (á, à, etc.) and underdots (ẹ, ọ, ṣ)
    are treated as unified single characters rather than isolated combining glyphs.
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Strip zero-width and invisible control characters
    cleaned = re.sub(r"[\u200b-\u200f\ufeff]", "", text)
    
    # 2. Normalise whitespace
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    
    # 3. Canonical Composition (NFC)
    return unicodedata.normalise("NFC", cleaned)

def audit_diacritic_density(text: str) -> float:
    """
    Calculates the ratio of tone-marked and sub-dotted characters relative to letters.
    Useful for flagging stripped or un-accented Yorùbá web text.
    """
    # Combining diacritics or explicit precomposed Yorùbá vowels/consonants
    yoruba_accented = re.findall(r"[áàéèẹ́ẹ̀íìóòọ́ọ̀úùṣÁÀÉÈẸ́Ẹ̀ÍÌÓÒỌ́Ọ̀ÚÙṢ]", text)
    letters = re.findall(r"[a-zA-Záàéèẹ́ẹ̀íìóòọ́ọ̀úùṣÁÀÉÈẸ́Ẹ̀ÍÌÓÒỌ́Ọ̀ÚÙṢ]", text)
    
    if not letters:
        return 0.0
    return len(yoruba_accented) / len(letters)