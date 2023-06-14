--
-- File generated with SQLiteStudio v3.4.3 on �� ��� 7 00:52:50 2023
--
-- Text encoding used: System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table: animal
DROP TABLE IF EXISTS animal;

CREATE TABLE IF NOT EXISTS animal (
    id   INT          PRIMARY KEY,
    name VARCHAR (50) 
);

INSERT INTO animal (id, name) VALUES (1, 'Cows');
INSERT INTO animal (id, name) VALUES (2, 'Chickens');

-- Table: chickens
DROP TABLE IF EXISTS chickens;

CREATE TABLE IF NOT EXISTS chickens (
    id        INT          PRIMARY KEY,
    name      VARCHAR (50),
    how_many_chickens      INT,
    howmuch   VARCHAR (50),
    dep_number INT,
    FOREIGN KEY (
        dep_number
    )
    REFERENCES animal (id) 
);


-- Table: cows
DROP TABLE IF EXISTS cows;

CREATE TABLE IF NOT EXISTS cows (
    id        INT          PRIMARY KEY,
    name      VARCHAR (50),
    code_cows VARCHAR(50),
    howmuch   VARCHAR (50),
    dep_number INT,
    FOREIGN KEY (
        dep_number
    )
    REFERENCES animal (id) 
);


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
