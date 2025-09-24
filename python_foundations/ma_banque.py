import datetime
from typing import List, Dict

class Compte:
    def __init__(self, nom: str, solde_initial: float, taux_interet: float, pin: str):
        self.nom = nom
        self.solde = solde_initial
        self.taux_interet = taux_interet
        self.pin = pin
        self.historique: List[str] = []
        self.derniere_application_interet = datetime.date.today()

    def verifier_pin(self, pin: str) -> bool:
        return self.pin == pin

    def deposer(self, montant: float) -> None:
        self.solde += montant
        self.historique.append(f"Dépôt de {montant}€ - Nouveau solde: {self.solde}€ le {datetime.date.today()} à {datetime.datetime.now().strftime('%H:%M:%S')}")

    def retirer(self, montant: float) -> bool:
        if self.solde >= montant:
            self.solde -= montant
            self.historique.append(f"Retrait de {montant}€ - Nouveau solde: {self.solde}€ le {datetime.date.today()} à {datetime.datetime.now().strftime('%H:%M:%S')}")
            return True
        return False

    def appliquer_interet(self) -> None:
        aujourd_hui = datetime.date.today()
        if aujourd_hui.month != self.derniere_application_interet.month:
            interet = self.solde * (self.taux_interet / 100)
            self.solde += interet
            self.historique.append(f"Intérêt appliqué: {interet}€ - Nouveau solde: {self.solde}€ le {aujourd_hui} à {datetime.datetime.now().strftime('%H:%M:%S')}")
            self.derniere_application_interet = aujourd_hui

class Utilisateur:
    def __init__(self, nom: str):
        self.nom = nom
        self.comptes: Dict[str, Compte] = {}

    def ajouter_compte(self, nom: str, solde_initial: float, taux_interet: float, pin: str) -> None:
        if nom not in self.comptes:
            self.comptes[nom] = Compte(nom, solde_initial, taux_interet, pin)
            print(f"Compte '{nom}' créé avec succès pour l'utilisateur {self.nom}.")
        else:
            print(f"Un compte avec le nom '{nom}' existe déjà pour cet utilisateur.")

    def obtenir_compte(self, nom: str, pin: str) -> Compte:
        if nom in self.comptes:
            compte = self.comptes[nom]
            if compte.verifier_pin(pin):
                print(f"Accès au compte '{nom}' réussi😊")
                return compte
            else:
                print("PIN incorrect.🫤")
        else:
            print(f"Le compte '{nom}' n'existe pas pour cet utilisateur.🛑")
        return None

class GestionnaireBanque:
    def __init__(self):
        self.utilisateurs: Dict[str, Utilisateur] = {}

    def creer_utilisateur(self, nom: str) -> None:
        if nom not in self.utilisateurs:
            self.utilisateurs[nom] = Utilisateur(nom)
            print(f"Utilisateur '{nom}' créé avec succès.")
        else:
            print(f"Un utilisateur avec le nom '{nom}' existe déjà.")

    def obtenir_utilisateur(self, nom: str) -> Utilisateur:
        if nom not in self.utilisateurs:
            print(f"L'utilisateur '{nom}' n'existe pas.")
            return None
        return self.utilisateurs.get(nom)

    def creer_compte(self, nom_utilisateur: str, nom_compte: str, solde_initial: float, taux_interet: float, pin: str) -> None:
        utilisateur = self.obtenir_utilisateur(nom_utilisateur)
        if utilisateur:
            utilisateur.ajouter_compte(nom_compte, solde_initial, taux_interet, pin)
        else:
            print(f"L'utilisateur '{nom_utilisateur}' n'existe pas.")

    def acceder_compte(self, nom_utilisateur: str, nom_compte: str, pin: str) -> Compte:
        utilisateur = self.obtenir_utilisateur(nom_utilisateur)
        if utilisateur:
            return utilisateur.obtenir_compte(nom_compte, pin)
        else:
            print(f"L'utilisateur '{nom_utilisateur}' n'existe pas.")
        return None

    def transferer(self, nom_utilisateur_source: str, nom_compte_source: str, nom_utilisateur_cible: str, nom_compte_cible: str, montant: float, pin: str) -> bool:
        compte_source = self.acceder_compte(nom_utilisateur_source, nom_compte_source, pin)
        compte_cible = self.acceder_compte(nom_utilisateur_cible, nom_compte_cible, "")  # PIN non nécessaire pour le compte cible
        if compte_source and compte_cible:
            if compte_source.retirer(montant):
                compte_cible.deposer(montant)
                print(f"Transfert de {montant}€ de '{nom_compte_source}' à '{nom_compte_cible}' effectué avec succès.")
                return True
            else:
                print("Solde insuffisant pour effectuer le transfert.")
        return False

    def afficher_details_comptes(self, nom_utilisateur: str) -> None:
        utilisateur = self.obtenir_utilisateur(nom_utilisateur)
        if utilisateur:
            print(f"Comptes de l'utilisateur {utilisateur.nom}:")
            for nom_compte, compte in utilisateur.comptes.items():
                print(f"  Compte: {nom_compte}")
                print(f"    Solde: {compte.solde}€")
                print(f"    Taux d'intérêt: {compte.taux_interet}%")
                print(f"    Dernière application d'intérêt: {compte.derniere_application_interet}")
                print()
        else:
            print(f"L'utilisateur '{nom_utilisateur}' n'existe pas.")

def menu_principal():
    print("\n----------------- Menu Principal -----------------")
    print("1. Créer un utilisateur")
    print("2. Se connecter en tant qu'utilisateur")
    print("3. 🔽 Quitter")
    return input("Choisissez une option: ")

def menu_utilisateur(nom_utilisateur: str):
    print(f"\n----------------- Menu Utilisateur: {nom_utilisateur} -----------------")
    print("1. Créer un compte")
    print("2. Accéder à un compte")
    print("3. Transférer de l'argent")
    print("4. Afficher les détails des comptes")
    print("5. 🔙 Retour au menu principal")
    return input("Choisissez une option: ")

def menu_compte():
    print("\n----------------- Menu du Compte -----------------")
    print("1. Consulter le solde")
    print("2. Déposer de l'argent")
    print("3. Retirer de l'argent")
    print("4. Afficher l'historique")
    print("5. 🔙 Retour au menu utilisateur")
    return input("Choisissez une option: ")

def main():
    banque = GestionnaireBanque()

    while True:
        choix = menu_principal()

        if choix == '1':
            nom_utilisateur = input("Nom de l'utilisateur: ")
            banque.creer_utilisateur(nom_utilisateur)

        elif choix == '2':
            nom_utilisateur = input("Nom de l'utilisateur: ")
            utilisateur = banque.obtenir_utilisateur(nom_utilisateur)
            if utilisateur:
                while True:
                    choix_utilisateur = menu_utilisateur(nom_utilisateur)
                    if choix_utilisateur == '1':
                        nom_compte = input("Nom du compte: ")
                        solde_initial = float(input("Solde initial: "))
                        taux_interet = float(input("Taux d'intérêt (%): "))
                        pin = input("Créez un code PIN: ")
                        banque.creer_compte(nom_utilisateur, nom_compte, solde_initial, taux_interet, pin)

                    elif choix_utilisateur == '2':
                        nom_compte = input("Nom du compte: ")
                        pin = input("Entrez le code PIN: ")
                        compte = banque.acceder_compte(nom_utilisateur, nom_compte, pin)
                        if compte:
                            while True:
                                choix_compte = menu_compte()
                                if choix_compte == '1':
                                    print(f"Solde actuel: {compte.solde}€")
                                elif choix_compte == '2':
                                    montant = float(input("Montant à déposer: "))
                                    compte.deposer(montant)
                                    print(f"Dépôt de {montant}€ effectué.")
                                elif choix_compte == '3':
                                    montant = float(input("Montant à retirer: "))
                                    if compte.retirer(montant):
                                        print(f"Retrait de {montant}€ effectué.")
                                    else:
                                        print("Solde insuffisant.")
                                elif choix_compte == '4':
                                    print("\nHistorique des transactions:")
                                    for transaction in compte.historique:
                                        print(transaction)
                                elif choix_compte == '5':
                                    break
                                else:
                                    print("Option invalide. Veuillez réessayer.")

                    elif choix_utilisateur == '3':
                        nom_compte_source = input("Nom du compte source: ")
                        nom_utilisateur_cible = input("Nom de l'utilisateur cible: ")
                        nom_compte_cible = input("Nom du compte cible: ")
                        montant = float(input("Montant à transférer: "))
                        pin = input("Entrez le code PIN du compte source: ")
                        banque.transferer(nom_utilisateur, nom_compte_source, nom_utilisateur_cible, nom_compte_cible, montant, pin)

                    elif choix_utilisateur == '4':
                        banque.afficher_details_comptes(nom_utilisateur)

                    elif choix_utilisateur == '5':
                        break

                    else:
                        print("Option invalide. Veuillez réessayer.")

        elif choix == '3':
            print("Merci d'avoir utilisé notre service bancaire. Au revoir!")
            break

        else:
            print("Option invalide. Veuillez réessayer.")

if __name__ == "__main__":
    main()