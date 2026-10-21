from src.normaliser import normalise_yoruba_text, audit_diacritic_density

class YorubaCorpusFilter:
    def __init__(self, nlp):
        self.nlp = nlp

    def audit_sentence(self, raw_text: str) -> dict:
        """
        Audits a single text string against syntactic and orthographic rules.
        """
        text = normalise_yoruba_text(raw_text)
        doc = self.nlp(text)
        total_tokens = len(doc)

        if total_tokens < 4:
            return {"is_valid": False, "reason": "TOO_SHORT", "text": text}

        # 1. Metric: Symbol / Noise Density
        noise_tokens = sum(1 for t in doc if t.text in "=+$#@%^&*<>[]{}|~`_")
        if (noise_tokens / total_tokens) > 0.15:
            return {"is_valid": False, "reason": "HIGH_SYMBOL_NOISE", "text": text}

        # 2. Metric: Grammatical Particle Ratio (Function words vs Content words)
        functional_tags = {"AUX", "DET", "ADP", "CCONJ", "SCONJ", "PRON"}
        particle_count = sum(1 for t in doc if t.pos_ in functional_tags)
        particle_ratio = particle_count / total_tokens

        # Natural Yorùbá sentences usually contain at least 20-30% functional particles.
        # Spam lists or broken noun sequences will have almost 0%.
        if particle_ratio < 0.15:
            return {"is_valid": False, "reason": "LOW_PARTICLE_DENSITY_SPAM", "text": text}

        # 3. Metric: Diacritic Completeness (Check for completely unaccented/degraded text)
        diacritic_score = audit_diacritic_density(text)
        if diacritic_score < 0.05:
            return {"is_valid": False, "reason": "MISSING_DIACRITICS", "text": text}

        return {
            "is_valid": True,
            "reason": "PASSED",
            "text": text,
            "tokens": total_tokens,
            "particle_ratio": round(particle_ratio, 2),
            "diacritic_density": round(diacritic_score, 2)
        }