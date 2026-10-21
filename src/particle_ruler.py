# Canonical closed-class inventory in Universal Dependencies (UD_Yoruba-YTB)
YORUBA_CLOSED_CLASSES = {
    "AUX": [
        "ti", "ń", "máa", "yóò", "maa", "yoo", "tiẹ̀", "kò", "kìí", "kọ̀", "bá", "le", "lè"
    ],
    "DET": [
        "náà", "naa", "yìí", "yii", "yi", "wọ̀nyí", "wọnyi", "wọ̀nyẹn", "wọnyen", "kan", "gbogbo"
    ],
    "ADP": [
        "ní", "ni", "sí", "si", "láti", "lati", "fún", "fun", "pẹ̀lú", "pelu", "nipa", "nípa"
    ],
    "CCONJ": [
        "àti", "ati", "tàbí", "tabi", "ṣùgbọ́n", "sugbon"
    ],
    "SCONJ": [
        "pé", "pe", "tí", "ti", "bí", "bi", "kí", "ki"
    ],
    "PRON": [
        "mo", "o", "ó", "a", "ẹ", "wọ́n", "mi", "rẹ", "rẹ̀", "wa", "yín", "wọn", "emi", "èmi", "iwo", "ìwọ", "oun", "òun"
    ]
}

def register_particle_rules(nlp):
    """
    Attaches an AttributeRuler component to the spaCy pipeline
    to assign POS tags to closed-class markers deterministically.
    """
    if "attribute_ruler" not in nlp.pipe_names:
        ruler = nlp.add_pipe("attribute_ruler")
    else:
        ruler = nlp.get_pipe("attribute_ruler")
        
    for pos_tag, tokens in YORUBA_CLOSED_CLASSES.items():
        for token_str in tokens:
            # Match both lower and upper casing
            patterns = [
                [{"LOWER": token_str.lower()}]
            ]
            attrs = {"POS": pos_tag}
            ruler.add(patterns=patterns, attrs=attrs)
            
    return nlp