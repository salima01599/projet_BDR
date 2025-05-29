import sqlite3

def insert_data():
    conn = sqlite3.connect("hotel.db")
    cur = conn.cursor()

    cur.execute("PRAGMA foreign_keys = OFF")
    cur.executescript("""
        DELETE FROM Evaluation;
        DELETE FROM Reservation_Chambre;
        DELETE FROM Reservation;
        DELETE FROM Chambre;
        DELETE FROM Type_Chambre;
        DELETE FROM Client;
        DELETE FROM Prestation;
        DELETE FROM Hotel;
    """)
    cur.execute("PRAGMA foreign_keys = ON")
    # Données Hotel
    cur.executemany("INSERT INTO Hotel VALUES (?, ?, ?, ?)", [
        (1, 'Paris', 'France', 75001),
        (2, 'Lyon', 'France', 69002)
    ])

    # Données Client
    cur.executemany("INSERT INTO Client VALUES (?, ?, ?, ?, ?, ?, ?)", [
        (1, '12 Rue de Paris', 'Paris', 75001, 'jean.dupont@email.fr', '0612345678', 'Jean Dupont'),
        (2, '5 Avenue Victor Hugo', 'Lyon', 69002, 'marie.leroy@email.fr', '0623456789', 'Marie Leroy'),
        (3, '8 Boulevard Saint-Michel', 'Marseille', 13005, 'paul.moreau@email.fr', '0634567890', 'Paul Moreau'),
        (4, '27 Rue Nationale', 'Lille', 59800, 'lucie.martin@email.fr', '0645678901', 'Lucie Martin'),
        (5, '3 Rue des Fleurs', 'Nice', 6000, 'emma.giraud@email.fr', '0656789012', 'Emma Giraud')
    ])

    # Données Prestation
    cur.executemany("INSERT INTO Prestation VALUES (?, ?, ?)", [
        (1, 15, 'Petit-déjeuner'),
        (2, 30, 'Navette aéroport'),
        (3, 0, 'Wi-Fi gratuit'),
        (4, 50, 'Spa et bien-être'),
        (5, 20, 'Parking sécurisé')
    ])

    # Données Type_Chambre
    cur.executemany("INSERT INTO Type_Chambre VALUES (?, ?, ?)", [
        (1, 'Simple', 80),
        (2, 'Double', 120)
    ])

    # Données Chambre
    cur.executemany("INSERT INTO Chambre VALUES (?, ?, ?, ?, ?, ?)", [
        (1, 201, 2, 0, 1, 1),
        (2, 502, 5, 1, 1, 2),
        (3, 305, 3, 0, 2, 1),
        (4, 410, 4, 0, 2, 2),
        (5, 104, 1, 1, 2, 2),
        (6, 202, 2, 0, 1, 1),
        (7, 307, 3, 1, 1, 2),
        (8, 101, 1, 0, 1, 1)
    ])

    # Données Réservation
    cur.executemany("INSERT INTO Reservation VALUES (?, ?, ?, ?)", [
        (1, '2025-06-15', '2025-06-18', 1),
        (2, '2025-07-01', '2025-07-05', 2),
        (3, '2025-08-10', '2025-08-14', 3),
        (4, '2025-09-05', '2025-09-07', 4),
        (5, '2025-09-20', '2025-09-25', 5),
        (7, '2025-11-12', '2025-11-14', 2),
        (9, '2026-01-15', '2026-01-18', 4),
        (10, '2026-02-01', '2026-02-05', 2)
    ])

    # Données Reservation_Chambre
    cur.executemany("INSERT INTO Reservation_Chambre VALUES (?, ?)", [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (7, 7),
        (9, 6),
        (10, 8)
    ])

    # Données Evaluation
    cur.executemany("INSERT INTO Evaluation VALUES (?, ?, ?, ?, ?)", [
        (1, '2025-06-15', 5, 'Excellent séjour, personnel très accueillant.', 1),
        (2, '2025-07-01', 4, 'Chambre propre, bon rapport qualité/prix.', 2),
        (3, '2025-08-10', 3, 'Séjour correct mais bruyant la nuit.', 3),
        (4, '2025-09-05', 5, 'Service impeccable, je recommande.', 4),
        (5, '2025-09-20', 4, 'Très bon petit-déjeuner, hôtel bien situé.', 5)
    ])

    conn.commit()
    conn.close()

if __name__ == "__main__":
    insert_data()
