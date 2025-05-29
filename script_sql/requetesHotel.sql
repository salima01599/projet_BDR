-- a. Afficher la liste des réservations avec le nom du client et la ville de l’hôtel réservé.
SELECT 
    Reservation.id_Reservation,
    Client.Nom,
    Hotel.ville
FROM 
    Reservation
JOIN Client ON Reservation.id_Client = Client.id_Client
JOIN Reservation_Chambre ON Reservation.id_Reservation = Reservation_Chambre.id_Reservation
JOIN Chambre ON Reservation_Chambre.id_Chambre = Chambre.id_Chambre
JOIN Hotel ON Chambre.id_Hotel = Hotel.id_Hotel;

-- b. Afficher les clients qui habitent à Paris.
SELECT *
FROM Client
WHERE ville_client = 'Paris';

-- c. Calculer le nombre de réservations faites par chaque client.
SELECT 
    Client.id_Client,
    Client.Nom,
    COUNT(Reservation.id_Reservation) AS nb_Reservations
FROM 
    Reservation
JOIN Client ON Reservation.id_Client = Client.id_Client
GROUP BY Client.id_Client, Client.Nom;

-- d. Donner le nombre de chambres pour chaque type de chambre.
SELECT 
    Type_Chambre.type_Chambre,
    COUNT(*) AS nb_chambres
FROM 
    Chambre
JOIN Type_Chambre ON Chambre.id_Type = Type_Chambre.id_Type
GROUP BY Type_Chambre.type_chambre;

-- e. Afficher la liste des chambres qui ne sont pas réservées pour une période donnée (entre deux dates saisies par l’utilisateur).
SELECT 
	Chambre.id_Chambre,
    Chambre.num_Chambre,
    Chambre.etage,
    Type_Chambre.type_chambre,
    Hotel.ville as ville_hotel
FROM Chambre
join Type_Chambre ON Chanbre.id_Type = Type_Chambre.id_Type
JOIN Hotel ON Chanbre.id_Hotel = Hotel.id_Hotel
WHERE Chambre.id_Chambre NOT IN (
    SELECT Reservation_Chambre.id_Chambre
    FROM Reservation
    JOIN Reservation_Chambre ON Reservation.id_Reservation = Reservation_Chambre.id_Reservation
    WHERE NOT (
        Reservation.date_depart <  @date_debut
        OR Reservation.date_arrivee >  @date_fin
    )
);