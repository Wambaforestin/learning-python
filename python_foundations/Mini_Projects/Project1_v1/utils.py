import string

PONCTUATIONS = string.punctuation
SEPARATEURS_PHRASES = [".", "!", "?"]

def nettoyer_texte(texte: str) -> str:
    # supprime la ponctuation, met en minuscule.
    texte = texte.translate(str.maketrans("", "", PONCTUATIONS))
    return texte.lower()

def split_en_mots(texte: str) -> list[str]:
    # sépare en mots
    return texte.split()

def split_en_phrases(texte: str) -> list[str]:
    # découpe en phrases by replacing all separators with a common one
    for sep in SEPARATEURS_PHRASES:
        texte = texte.replace(sep, '|')
    phrases = texte.split('|')
    return [phrase.strip() for phrase in phrases if phrase.strip()]
