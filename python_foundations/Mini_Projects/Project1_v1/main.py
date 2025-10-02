from utils import nettoyer_texte, split_en_mots, split_en_phrases
from analysis import compter_mots, compter_phrases, mot_plus_frequent, longueur_moyenne_mots

if __name__ == "__main__":
    # Demander à l'utilisateur de saisir un text
    sentence = input("Veuillez saisir une phrase : ")
    
    # appeler les fonctions nécessaire pour nettqyer le text
    cleaned_text = nettoyer_texte(sentence)
    liste_words = split_en_mots(cleaned_text)
    liste_phrases = split_en_phrases(sentence)

    # appeler les fonctions d'analyse pour extraire les stats
    word_count = compter_mots(cleaned_text)
    phrase_count = compter_phrases(sentence)
    most_frequent_word, frequency = mot_plus_frequent(liste_words)
    average_word_length = longueur_moyenne_mots(liste_words)

    # Afficher les résultats
    print(f"Nombre de mots : {word_count}")
    print(f"Nombre de phrases : {phrase_count}")
    print(f"Mot le plus fréquent : {most_frequent_word} (fréquence : {frequency})")
    print(f"Longueur moyenne des mots : {average_word_length:.2f}")