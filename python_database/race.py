#Exercice des vaisseaux
# Vous devez modéliser une course de vaisseaux spatiaux.
# Ces vaisseaux ont comme particularité un nom, une couleur, une vitesse nominale (m/s) et une latence (s). 
# Les vaisseaux évoluent sur un circuit qui a une distance en mètres et un nombre de tours.
# Pour une course donnée, à chaque tick (s), indiquer la position des vaisseaux.
# Sauvegarder la position des vaisseaux en BDD à chaque tick.

# Pseudo-code
# Classe Vaisseau :
# - Attributs : nom, couleur, vitesse, latence, position
# - Méthode : avancer(distance) qui met à jour la position du vaisseau
# Classe Course :
# - Attributs : circuit (distance, tours), vaisseaux
# - Méthode : tick() qui fait avancer tous les vaisseaux d'une certaine distance
# - Méthode : sauvegarder_positions() qui enregistre les positions des vaisseaux en BDD
# - Méthode : afficher_positions() qui affiche les positions actuelles des vaisseaux
# - Méthode : demarrer() qui lance la course et appelle tick() à intervalles rég
# - Méthode : terminer() qui arrête la course et sauvegarde les positions finales

import time
import sqlite3

# Classe représentant un vaisseau spatial
class Vaisseau:
    def __init__(self, nom, vitesse):
        # Initialisation des attributs du vaisseau
        self.nom = nom          
        self.vitesse = vitesse 
        self.position = 0       

    def avancer(self, duree):
        # Calcul de la nouvelle position en fonction de la vitesse et du temps
        self.position = self.vitesse + self.position * duree

class Course:
    def __init__(self, distance_totale):
        # Initialisation de la course
        self.distance_totale = distance_totale  # Distance totale à parcourir
        self.vaisseaux =  set()
        # Connexion à la base de données SQLite
        self.connexion = sqlite3.connect('course.db')
        
        # Création de la table pour stocker les positions
        self.creer_base_donnees()

    def creer_base_donnees(self):
        # Création de la table des positions si elle n'existe pas
       try:
            curseur = self.connexion.cursor()
            curseur.execute('''CREATE TABLE positions (
                temps INTEGER,
                vaisseau TEXT,
                position REAL
            )''')
            self.connexion.commit()  # Validation de la création
       except sqlite3.OperationalError:
            # La table existe déjà
            print("La table des positions existe déjà.")
       except Exception as e:
            print(f"Erreur lors de la création de la base de données : {e}")
            
    def ajouter_vaisseau(self, vaisseau):
        # Ajouter un vaisseau à la course
        self.vaisseaux.add(vaisseau)

    def derouler_course(self):
        # Méthode principale pour simuler la course
        temps = 0  # Compteur de temps
        
        # Continuer tant qu'aucun vaisseau n'a atteint la distance totale
        while all(vaisseau.position < self.distance_totale for vaisseau in self.vaisseaux):
            # Faire avancer chaque vaisseau
            for vaisseau in self.vaisseaux:
                vaisseau.avancer(1)  # Avancer de 1 seconde
                
                # Sauvegarder et afficher la position
                self.sauvegarder_position(temps, vaisseau)
                print(f"{vaisseau.nom}: {vaisseau.position} mètres")
            
            temps += 1  # Incrémenter le temps
            time.sleep(1)  # Pause d'une seconde entre chaque tick
        
        print("Course terminée !")

    def sauvegarder_position(self, temps, vaisseau):
        # Enregistrer la position du vaisseau dans la base de données
        curseur = self.connexion.cursor()
        curseur.execute('''
            INSERT INTO positions (temps, vaisseau, position)
            VALUES (?, ?, ?)
        ''', (temps, vaisseau.nom, vaisseau.position))
        self.connexion.commit()  # Valider l'insertion

# Exemple d'utilisation de la simulation
course = Course(distance_totale=100)  # Créer une course de 1000 mètres
course.ajouter_vaisseau(Vaisseau("Fusée Rouge", 10))  # Ajouter un vaisseau
course.ajouter_vaisseau(Vaisseau("Fusée Bleue", 15))  # Ajouter un second vaisseau
course.derouler_course()  # Démarrer la course