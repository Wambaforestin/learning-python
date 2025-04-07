from __future__ import annotations  # pour auto definitions

import uuid
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional


@dataclass
class Affectation:
    """Hiérarchie de catégorisation des paiements.

    exemple : Loisirs -> Sports -> Foot ou Logement -> Loyer
    """

    titre: str
    parent: Optional[Affectation] = None
    enfants: Optional[List[Affectation]] = None


@dataclass
class Compte:
    """Comptes bancaires"""

    _id: str
    nom: str
    banque: str


@dataclass
class Montant:
    """Couple valeur/monnaie pour le montant payé/reçu."""

    valeur: str
    monnaie: Optional[str] = "EUR"


@dataclass
class Adresse:

    adresse: str
    code_postal: str
    ville: str


@dataclass
class Tiers:
    """Entreprise ou personne source/cible de la Transaction"""

    nom: str
    adresse: Adresse


@dataclass
class Transaction:
    """Transfert d'argent entre mon compte et un tiers."""

    libelle: str
    date: datetime
    compte: Compte
    montant: Montant
    affectations: Optional[List[Affectation]] = (
        None  # Partie source/cible de la comptabilité en partie double
    )
    uuid: Optional[str] = None
    tiers: Optional[Tiers] = None

    def gen_uuid(self):
        self.uuid = str(uuid.uuid4())
