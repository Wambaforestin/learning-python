## PROJET 1 : Analyseur de Texte Interactif

### Description

Un programme CLI qui analyse un texte saisi par l’utilisateur (ou collé) et fournit des statistiques : nombre de mots, de phrases, fréquence des mots, mots les plus longs, etc.

### Valeur Portfolio

Montre une capacité d’analyse de données textuelles, compétence très recherchée (data cleaning, NLP).

### Concepts Python Pratiqués

Boucles et conditions

Chaînes de caractères (split, count, replace)

Dictionnaires (fréquences de mots)

Module string (ponctuation)

### Fonctionnalités Principales

Compter le nombre de mots et de phrases

Trouver le mot le plus fréquent

Identifier la longueur moyenne des mots

Option avancée : afficher un petit histogramme textuel des fréquences

### Architecture

main.py         # Menu principal
utils.py        # Fonctions de nettoyage/normalisation
analysis.py     # Fonctions statistiques
constants.py    # Caractères à ignorer, stopwords

### Complexité

Durée estimée : 1-2 jours

Difficulté : Débutant+

Lignes de code : ~120-150

### Extensions Possibles

POO : Classe TextAnalyzer

Fichiers : charger un texte depuis .txt
