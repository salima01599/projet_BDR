import sqlite3

def create_db():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()

    # Table Hotel
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Hotel (
            id_hotel INTEGER PRIMARY KEY,
            ville TEXT,
            pays TEXT,
            code_postal INTEGER
        );
    """)

    # Table Client
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Client (
            id_client INTEGER PRIMARY KEY,
            adresse TEXT,
            ville TEXT,
            code_postal INTEGER,
            email TEXT,
            telephone TEXT,
            nom_client TEXT
        );
    """)

    # Table Prestation
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Prestation (
            id_prestation INTEGER PRIMARY KEY,
            prix REAL,
            description TEXT
        );
    """)

    # Table Type_Chambre
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Type_Chambre (
            id_type INTEGER PRIMARY KEY,
            nom_type TEXT,
            prix REAL
        );
    """)

    # Table Chambre
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Chambre (
            id_chambre INTEGER PRIMARY KEY,
            numero_chambre INTEGER,
            etage INTEGER,
            balcon INTEGER,
            id_type INTEGER,
            id_hotel INTEGER,
            FOREIGN KEY (id_type) REFERENCES Type_Chambre(id_type),
            FOREIGN KEY (id_hotel) REFERENCES Hotel(id_hotel)
        );
    """)

    # Table Reservation
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Reservation (
            id_reservation INTEGER PRIMARY KEY,
            date_arrivee TEXT,
            date_depart TEXT,
            id_client INTEGER,
            FOREIGN KEY (id_client) REFERENCES Client(id_client)
        );
    """)

    # Table Reservation_Chambre (relation N-N)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Reservation_Chambre (
            id_reservation INTEGER,
            id_chambre INTEGER,
            PRIMARY KEY (id_reservation, id_chambre),
            FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation),
            FOREIGN KEY (id_chambre) REFERENCES Chambre(id_chambre)
        );
    """)

    # Table Evaluation
    cur.execute("""
        CREATE TABLE IF NOT EXISTS Evaluation (
            id_evaluation INTEGER PRIMARY KEY,
            date_evaluation TEXT,
            note INTEGER,
            commentaire TEXT,
            id_reservation INTEGER,
            FOREIGN KEY (id_reservation) REFERENCES Reservation(id_reservation)
        );
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    create_db()
