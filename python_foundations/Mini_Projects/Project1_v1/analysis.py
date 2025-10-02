from utils import nettoyer_texte, split_en_mots, split_en_phrases
def compter_mots(texte: str) -> int:
    # compte le nombre de mots
    return len(split_en_mots(nettoyer_texte(texte)))

def compter_phrases(texte: str) -> int:
    # compte le nombre de phrases
    return len(split_en_phrases(texte))

def mot_plus_frequent(mots: list[str]) -> tuple[str, int]:
    # recupère le nombre de mots avec leurs frequences
    frequences = {}
    for mot in mots:
        frequences[mot] = frequences.get(mot, 0) + 1
    mot, freq = max(frequences.items(), key=lambda x: x[1], default=("", 0))
    return mot, freq

def longueur_moyenne_mots(mots: list[str]) -> float:
    # calcule la longuer moyenne des mots
    if not mots:
        return 0.0
    return sum(len(mot) for mot in mots) / len(mots)

def afficher_histogramme(frequences: dict):
    # affiche un histogramme simple sur le terminal
    for mot, freq in frequences.items():
        print(f"{mot}: {'*' * freq}")