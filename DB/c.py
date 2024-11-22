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
