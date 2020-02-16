
CREATE TABLE bookmaker (
                id INT AUTO_INCREMENT NOT NULL,
                nom VARCHAR(255) NOT NULL,
                logo LONGBLOB,
                PRIMARY KEY (id)
);

CREATE TABLE utilisateur (
                id INT AUTO_INCREMENT NOT NULL,
                nom VARCHAR(255) NOT NULL,
                argent INT NOT NULL,
                mot_de_passe VARCHAR(255) NOT NULL,
                PRIMARY KEY (id)
);

CREATE TABLE favori (
                id INT AUTO_INCREMENT NOT NULL,
                requete VARCHAR(255) NOT NULL,
                utilisateur_id INT NOT NULL,
                PRIMARY KEY (id)
);


CREATE TABLE sport (
                Id INT AUTO_INCREMENT NOT NULL,
                nom VARCHAR(255) NOT NULL,
                logo LONGBLOB,
                PRIMARY KEY (Id)
);

CREATE TABLE resultat (
                Id INT AUTO_INCREMENT NOT NULL,
                statut VARCHAR(255),
                PRIMARY KEY (Id)
);


CREATE TABLE rencontre (
                id INT AUTO_INCREMENT NOT NULL,
                competition VARCHAR(255) NOT NULL,
                cote_match_nul DECIMAL(10,2),
                equipe_domicile VARCHAR(255) NOT NULL,
                cote_domicile DECIMAL(10,2),
                equipe_exterieure VARCHAR(255) NOT NULL,
                cote_exterieure DECIMAL(10,2),
                sport_id INT NOT NULL,
                diffuseur VARCHAR(255),
                region VARCHAR(255),
                date_affrontement DATETIME NOT NULL,
                date_scraping DATETIME NOT NULL,
                bookmaker_id INT NOT NULL,
                match_reference VARCHAR(255),
                resultat_id INT,
                PRIMARY KEY (id)
);

CREATE TABLE paris (
                id INT AUTO_INCREMENT NOT NULL,
                rencontre_id INT NOT NULL,
                utilisateur_id INT NOT NULL,
                cote DECIMAL(10,2) NOT NULL,
                verifie BOOLEAN NOT NULL default 0,
                date_enregistrement TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                mise INT,
                equipe_pariee INT NOT NULL,
                PRIMARY KEY (id)
);


--- Foreign keys rencontre ---
ALTER TABLE rencontre ADD CONSTRAINT bookmaker_match_fk
FOREIGN KEY (bookmaker_id)
REFERENCES bookmaker (id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE rencontre ADD CONSTRAINT sport_match_fk
FOREIGN KEY (sport_id)
REFERENCES sport (Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

--- Foreign keys paris ---
ALTER TABLE paris ADD CONSTRAINT rencontre_fk
FOREIGN KEY (rencontre_id)
REFERENCES rencontre (Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE paris ADD CONSTRAINT equipe_pariee_fk
FOREIGN KEY (equipe_pariee)
REFERENCES resultat (Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;

ALTER TABLE paris ADD CONSTRAINT utilisateur_fk
FOREIGN KEY (utilisateur_id)
REFERENCES utilisateur (Id)
ON DELETE NO ACTION
ON UPDATE NO ACTION;
