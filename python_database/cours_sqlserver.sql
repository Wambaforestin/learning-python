/* 
cours d'sqlserver : Apprendre à manipuler les bases de données avec SQL Server et les requêtes SQL
*/

-- Définition des termes
/* 
SGBD : Système de Gestion de Base de Données (SQL Server, MySQL, Oracle, PostgreSQL, SQLite, etc.)
Base de données : ensemble de données organisées et structurées en tables
Table/Entité : ensemble de données organisées en lignes et colonnes
Ligne : enregistrement dans une table
Colonne : champ dans une table
Clé primaire : colonne qui identifie de manière unique chaque ligne d'une table
Clé étrangère : colonne qui permet de lier deux tables entre elles
Contrainte : règle qui doit être respectée pour insérer ou modifier des données dans une table
Index : structure de données qui permet d'accélérer les recherches dans une table
Vue : requête SQL stockée dans la base de données
Procédure stockée : ensemble d'instructions SQL stockées dans la base de données
Déclencheur : ensemble d'instructions SQL qui s'exécutent automatiquement en réponse à un événement
Transaction : ensemble d'instructions SQL qui doivent être
---------------------------------------------------------------------
LDD : Langage de Définition de Données, par exemple : CREATE DATABASE, CREATE TABLE 
LMD : Langage de Manipulation de Données, par exemple : INSERT, UPDATE, DELETE
LCD : Langage de Contrôle de Données, par exemple : GRANT, REVOKE
LTD : Langage de Transaction de Données, par exemple : COMMIT, ROLLBACK
DQL : Data Query Language, par exemple : SELECT

Différence entre une procédure stockée et une fonction stockée :
- Une procédure stockée peut retourner zéro, un ou plusieurs résultats
- Une fonction stockée retourne un seul résultat
- Une procédure stockée peut modifier les données dans la base de données
- Une fonction stockée ne peut pas modifier les données dans la base de données
- Une procédure stockée peut appeler une fonction stockée
- Une fonction stockée ne peut pas appeler une procédure stockée
- Une procédure stockée peut être appelée directement
- Une fonction stockée doit être appelée dans une requête SELECT

*/

--montrer les bases de données
SELECT name FROM sys.databases

-- Créer une base de données
CREATE DATABASE IF NOT EXISTS cours_sqlserver;

-- Utiliser la base de données
USE cours_sqlserver;

-- Montrer les tables d'une base de données
SELECT * FROM information_schema.tables

-- Créer une table
CREATE TABLE IF NOT EXISTS clients (
    id INT PRIMARY KEY IDENTITY(1,1),
    nom VARCHAR(50),
    prenom VARCHAR(50),
    email VARCHAR(100)
);

--Créer une table avec une clé étrangère
CREATE TABLE IF NOT EXISTS commandes (
    id INT PRIMARY KEY,
    date_commande DATE,
    id_client INT,
    FOREIGN KEY (id_client) REFERENCES clients(id)
);

-- ou bien
CREATE TABLE IF NOT EXISTS commandes (
    id INT PRIMARY KEY,
    date_commande DATE,
    id_client INT,
    CONSTRAINT fk_client FOREIGN KEY (id_client) REFERENCES clients(id)
);
-- ou bien
CREATE TABLE IF NOT EXISTS commandes (
    id INT PRIMARY KEY,
    date_commande DATE,
    id_client INT,
);
ALTER TABLE commandes ADD CONSTRAINT fk_client FOREIGN KEY (id_client) REFERENCES clients(id);

-- Insérer des données dans une table
INSERT INTO clients (id, nom, prenom, email) VALUES (1, 'Doe', 'John', 'example@gmail.com');

-- Mise à jour des données dans une table
UPDATE clients SET nom = 'Smith' WHERE id = 1;
-- Supprimer des données dans une table
DELETE FROM clients WHERE id = 1;
-- Sélectionner des données dans une table
SELECT * FROM clients;
-- Sélectionner des données spécifiques dans une table
SELECT nom, prenom FROM clients;
-- Sélectionner des données avec une condition
SELECT * FROM clients WHERE nom = 'Doe';
-- Sélectionner des données avec une condition
SELECT * FROM clients WHERE nom LIKE 'D%';
-- Sélectionner des données avec une condition

-- Supprimer une table
DROP TABLE IF EXISTS clients;

-- Supprimer une base de données
DROP DATABASE IF EXISTS cours_sqlserver;

-- Autre ORDER BY, GROUP BY, HAVING, JOIN, UNION, INTERSECT, EXCEPT, LIMIT, OFFSET, DISTINCT ,TRUNCATE etc.
-- exemple de requête avec ORDER BY (tri des données)
SELECT nom, prenom FROM clients ORDER BY nom ASC;
-- exemple de requête avec GROUP BY (regrouper les données)
SELECT nom, COUNT(*) AS total FROM clients GROUP BY nom;
-- exemple de requête avec HAVING (condition sur le résultat de GROUP BY)
SELECT nom, COUNT(*) AS total FROM clients GROUP BY nom HAVING total > 1;
-- exemple de requête avec DISTINCT (élimine les doublons)
SELECT DISTINCT nom FROM clients;
-- exemple de requête avec TRUNCATE (vide une table)
TRUNCATE TABLE clients;
-- exemple de requête avec UNION (combine les résultats de deux requêtes qui ont le même nombre de colonnes)
SELECT nom FROM clients UNION SELECT nom FROM commandes;
-- exemple de requête avec INTERSECT (combine les résultats de deux requêtes en ne gardant que les lignes communes)
SELECT nom FROM clients INTERSECT SELECT nom FROM commandes;

-- mise a jour d'un attribut
UPDATE clients SET nom = 'Doe', prenom = 'John' WHERE id = 1;
-- suppression d'un attribut
DELETE FROM clients WHERE id = 1;
-- ajout d'une contrainte sur un attribut specifique
ALTER TABLE clients ADD CONSTRAINT email_unique UNIQUE (email);
-- suppression d'une contrainte sur un attribut specifique
ALTER TABLE clients DROP CONSTRAINT email_unique;
-- ajout d'une colonne
ALTER TABLE clients ADD telephone VARCHAR(20);
-- suppression d'une colonne
ALTER TABLE clients DROP COLUMN telephone;
-- renommer une colonne
ALTER TABLE clients RENAME COLUMN nom TO nom_client;
-- renommer une table
ALTER TABLE clients RENAME TO customers;


-- Autre UPPER, LOWER, LENGTH, SUBSTRING, REPLACE, TRIM, CONCAT, NOW, CURDATE, CURTIME, etc.
-- exemple de requête avec UPPER (convertit une chaîne de caractères en majuscules)
SELECT UPPER(nom) FROM clients;
-- exemple de requête avec LOWER (convertit une chaîne de caractères en minuscules)
SELECT LOWER(nom) FROM clients;
-- exemple de requête avec LENGTH (retourne la longueur d'une chaîne de caractères)
SELECT LENGTH(nom) FROM clients;
-- exemple de requête avec SUBSTRING (retourne une partie d'une chaîne de caractères)
SELECT SUBSTRING(nom, 1, 3) FROM clients;
-- exemple de requête avec REPLACE (remplace une partie d'une chaîne de caractères par une autre)
SELECT REPLACE(nom, 'Doe', 'Smith') FROM clients;
-- exemple de requête avec TRIM (supprime les espaces en début et fin de chaîne de caractères)
SELECT TRIM(nom) FROM clients;
-- exemple de requête avec CONCAT (concatène plusieurs chaînes de caractères)
SELECT CONCAT(nom, ' ', prenom) FROM clients;
-- exemple de requête avec NOW (retourne la date et l'heure actuelles)
SELECT NOW();
-- exemple de requête avec CURDATE (retourne la date actuelle)
SELECT CURDATE();
-- exemple de requête avec CURTIME (retourne l'heure actuelle)
SELECT CURTIME();

-- les Jointures en SQLSERVER

-- INNER JOIN : retourne les lignes lorsque qu'il y a au moins une correspondance dans les deux tables
SELECT clients.nom, commandes.date_commande 
FROM clients
INNER JOIN commandes ON clients.id = commandes.id_client;

-- LEFT JOIN : retourne toutes les lignes de la table de gauche et les lignes correspondantes de la table de droite
SELECT clients.nom, commandes.date_commande
FROM clients
LEFT JOIN commandes ON clients.id = commandes.id_client;

-- RIGHT JOIN : retourne toutes les lignes de la table de droite et les lignes correspondantes de la table de gauche
SELECT clients.nom, commandes.date_commande
FROM clients
RIGHT JOIN commandes ON clients.id = commandes.id_client;

-- FULL JOIN : retourne toutes les lignes lorsque qu'il y a une correspondance dans une des deux tables
SELECT clients.nom, commandes.date_commande
FROM clients
FULL JOIN commandes ON clients.id = commandes.id_client;

-- UNION : permet de combiner les résultats de deux requêtes SQL en une seule
SELECT nom FROM clients
UNION
SELECT nom FROM commandes;

-- INTERSECT : permet de combiner les résultats de deux requêtes SQL en une seule en ne gardant que les lignes communes (c'est-à-dire les lignes qui apparaissent dans les deux résultats)
SELECT nom FROM clients
INTERSECT
SELECT nom FROM commandes;

-- les sous-requêtes en SQLSERVER
-- exemple de sous-requête dans une clause WHERE
SELECT nom, prenom
FROM clients
WHERE id IN (SELECT id_client FROM commandes WHERE date_commande = '2022-01-01');

-- Différence entre une sous-requête et une jointure
-- Une sous-requête est une requête imbriquée dans une autre requête
-- Une jointure est une opération qui combine les lignes de deux tables en fonction d'une condition de correspondance entre les colonnes de ces tables
-- Une sous-requête est généralement utilisée pour filtrer les résultats d'une requête principale
-- Une jointure est généralement utilisée pour combiner les données de deux tables en une seule requête


/*
 Boutique de vente de jeux de société en ligne : 
 donner les diffrérentes tables à créer : produits, clients, commandes, catégories, etc.
 Association entre les tables : 
  - un client peut passer une ou plusieurs commandes et une commande est passée par un seul client (1,n relation-> 1,1 relation)
  - un produit appartient à une seule catégorie et une catégorie peut contenir plusieurs produits (exemple de catégories : jeux de cartes, jeux de rôle, etc.)
  CODE simplifier pour la création du MCD (Modèle Conceptuel de Données) avec l'outil mocodo online

  ```
  CLIENT: email
  COMMANDER, 0N CLIENT, 1N PRODUIT: quantité, date commande
  PRODUIT: titre,editeur
  APPARTENIR, 1N PRODUIT, 0N CATEGORIE
  CATEGORIE: nom
  ```

  Table de faits : table qui contient les données à analyser (ex : commandes)
  Table de dimensions/réference : table qui contient les informations détaillées sur les données (ex : clients, produits, catégories)
  Table de jointure : table qui permet de lier les tables de faits et de dimensions (ex : commandes_produits)
*/

