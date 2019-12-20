
CREATE TABLE bookmaker (
                id INT AUTO_INCREMENT NOT NULL,
                nom VARCHAR(255) NOT NULL,
                logo LONGBLOB,
                PRIMARY KEY (id)
);


CREATE TABLE sport (
                Id INT AUTO_INCREMENT NOT NULL,
                nom VARCHAR(255) NOT NULL,
                logo LONGBLOB,
                PRIMARY KEY (Id)
);


CREATE TABLE rencontre (
                id INT AUTO_INCREMENT NOT NULL,
                competition VARCHAR(255) NOT NULL,
                cote_match_nul DECIMAL(10,2) NOT NULL,
                equipe_domicile VARCHAR(255) NOT NULL,
                cote_domicile DECIMAL(10,2) NOT NULL,
                equipe_exterieure VARCHAR(255) NOT NULL,
                cote_exterieure DECIMAL(10,2) NOT NULL,
                sport_id INT NOT NULL,
                diffuseur VARCHAR(255),
                region VARCHAR(255) NOT NULL,
                date_affrontement DATETIME NOT NULL,
                date_scraping DATETIME NOT NULL,
                bookmaker_id INT NOT NULL,
                PRIMARY KEY (id)
);


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
