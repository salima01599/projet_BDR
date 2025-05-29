CREATE DATABASE IF NOT EXISTS creHotel;
USE creHotel;

CREATE TABLE Hotel (
    id_Hotel NUMERIC PRIMARY KEY,
    ville VARCHAR(50),
    pays VARCHAR(50),
    code_postal NUMERIC
);

CREATE TABLE Type_Chambre (
    id_Type NUMERIC PRIMARY KEY,
    type_chambre VARCHAR(20),
    tarif NUMERIC NOT NULL
);

CREATE TABLE Client (
    id_Client NUMERIC PRIMARY KEY,
    adresse VARCHAR(100),
    ville_client VARCHAR(50),
    code_postal_client NUMERIC,
    e_mail VARCHAR(100),
    num_tele NUMERIC,
    Nom VARCHAR(100)
);

CREATE TABLE Chambre (
    id_Chambre NUMERIC PRIMARY KEY,
    num_Chambre NUMERIC NOT NULL,
    etage NUMERIC,
    fumeur BOOL,
    id_Hotel NUMERIC,
    id_Type NUMERIC,
    CONSTRAINT fk_chambre_Hotel FOREIGN KEY (id_Hotel) REFERENCES Hotel (id_Hotel) ,
    CONSTRAINT fk_type_Hotel FOREIGN KEY (id_Type) REFERENCES Type_Chambre (id_Type)
);

CREATE TABLE Prestation (
    id_Prestation NUMERIC PRIMARY KEY,
    prix NUMERIC NOT NULL,
    type VARCHAR(30)
);

CREATE TABLE Offre (
    id_Hotel NUMERIC,
    id_Prestation NUMERIC,
    CONSTRAINT fk_offre_Hotel FOREIGN KEY (id_Hotel) REFERENCES Hotel (id_Hotel),
    CONSTRAINT fk_offre_prestation FOREIGN KEY (id_Prestation) REFERENCES Prestation (id_Prestation)
);

CREATE TABLE Reservation (
    id_Reservation NUMERIC PRIMARY KEY,
    date_arrivee DATE,
    date_depart DATE,
    id_Client NUMERIC,
    CONSTRAINT fk_Client_Reservation FOREIGN KEY (id_Client) REFERENCES Client (id_Client)
);

CREATE TABLE Evaluation (
    id_Evaluation NUMERIC PRIMARY KEY,
    date_arrivee DATE,
    note NUMERIC,
    texte_desc VARCHAR(5000),
    id_Hotel NUMERIC,
    id_Client NUMERIC,
    CONSTRAINT fk_evaluation_hotel FOREIGN KEY (id_Hotel) REFERENCES Hotel (id_Hotel) ,
    CONSTRAINT fk_evaluation_client FOREIGN KEY (id_Client) REFERENCES Client (id_Client)
);
 
CREATE TABLE concerner (
    id_Type NUMERIC,
    id_Reservation NUMERIC,
    CONSTRAINT fk_concerner_Type FOREIGN KEY (id_Type) REFERENCES Type_Chambre (id_Type) ,
    CONSTRAINT fk_concerner_Reservation FOREIGN KEY (id_Reservation) REFERENCES Reservation (id_Reservation)
);
CREATE TABLE Reservation_Chambre (
    id_Reservation NUMERIC,
    id_Chambre NUMERIC,
    PRIMARY KEY (id_Reservation, id_Chambre),
    CONSTRAINT fk_reservation FOREIGN KEY (id_Reservation) REFERENCES Reservation(id_Reservation),
    CONSTRAINT fk_chambre FOREIGN KEY (id_Chambre) REFERENCES Chambre(id_Chambre)
);