import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, date

# Configuration de la page
st.set_page_config(
    page_title="Gestion Hôtelière",
    page_icon="🏨",
    layout="wide"
)

# Connexion à la base de données
@st.cache_resource
def init_connection():
    return sqlite3.connect("hotel.db", check_same_thread=False)

conn = init_connection()

# Titre principal
st.title("🏨 Système de Gestion Hôtelière")
st.markdown("**Projet Bases de Données 2025 - Licence MIP-IAP S4**")
st.divider()

# Menu sidebar
menu = ["🏠 Accueil", "📋 Réservations", "👥 Clients", "🛏️ Chambres Disponibles", "➕ Ajouter Client", "📝 Ajouter Réservation"]
choix = st.sidebar.selectbox("Navigation", menu)

# Page d'accueil
if choix == "🏠 Accueil":
    st.header("Bienvenue dans le Système de Gestion Hôtelière")
    
    # Statistiques rapides
    col1, col2, col3, col4 = st.columns(4)
    
    try:
        # Nombre total de clients
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM Client")
        nb_clients = cur.fetchone()[0]
        
        # Nombre total de réservations
        cur.execute("SELECT COUNT(*) FROM Reservation")
        nb_reservations = cur.fetchone()[0]
        
        # Nombre total de chambres
        cur.execute("SELECT COUNT(*) FROM Chambre")
        nb_chambres = cur.fetchone()[0]
        
        # Nombre d'hôtels
        cur.execute("SELECT COUNT(*) FROM Hotel")
        nb_hotels = cur.fetchone()[0]
        
        with col1:
            st.metric("👥 Clients", nb_clients)
        with col2:
            st.metric("📋 Réservations", nb_reservations)
        with col3:
            st.metric("🛏️ Chambres", nb_chambres)
        with col4:
            st.metric("🏨 Hôtels", nb_hotels)
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des statistiques : {e}")
    
    st.info("👈 Utilisez le menu de navigation pour accéder aux différentes fonctionnalités.")

# Page des réservations
elif choix == "📋 Réservations":
    st.header("Liste des Réservations")
    
    try:
        query = """
        SELECT 
            r.id_reservation,
            c.nom_client,
            r.date_arrivee,
            r.date_depart,
            ch.numero_chambre,
            h.ville as ville_hotel
        FROM Reservation r 
        JOIN Client c ON r.id_client = c.id_client
        JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
        JOIN Chambre ch ON rc.id_chambre = ch.id_chambre
        JOIN Hotel h ON ch.id_hotel = h.id_hotel
        ORDER BY r.date_arrivee DESC
        """
        
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            # Formatage des colonnes
            df.columns = ['ID Réservation', 'Client', 'Arrivée', 'Départ', 'N° Chambre', 'Ville Hôtel']
            st.dataframe(df, use_container_width=True)
            
            # Bouton de téléchargement
            csv = df.to_csv(index=False)
            st.download_button(
                label="📥 Télécharger en CSV",
                data=csv,
                file_name="reservations.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucune réservation trouvée.")
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des réservations : {e}")

# Page des clients
elif choix == "👥 Clients":
    st.header("Liste des Clients")
    
    # Filtre par ville
    col1, col2 = st.columns([1, 3])
    with col1:
        villes_query = "SELECT DISTINCT ville FROM Client ORDER BY ville"
        villes = pd.read_sql_query(villes_query, conn)['ville'].tolist()
        ville_filtre = st.selectbox("Filtrer par ville", ["Toutes"] + villes)
    
    try:
        if ville_filtre == "Toutes":
            query = "SELECT * FROM Client ORDER BY nom_client"
        else:
            query = f"SELECT * FROM Client WHERE ville = '{ville_filtre}' ORDER BY nom_client"
        
        df = pd.read_sql_query(query, conn)
        
        if not df.empty:
            # Formatage des colonnes
            df.columns = ['ID', 'Adresse', 'Ville', 'Code Postal', 'Email', 'Téléphone', 'Nom']
            # Réorganiser les colonnes
            df = df[['ID', 'Nom', 'Ville', 'Adresse', 'Code Postal', 'Email', 'Téléphone']]
            st.dataframe(df, use_container_width=True)
            
            # Statistiques
            st.subheader("📊 Statistiques")
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Nombre total de clients", len(df))
            with col2:
                ville_counts = df['Ville'].value_counts()
                st.write("**Répartition par ville :**")
                st.write(ville_counts)
        else:
            st.info("Aucun client trouvé.")
            
    except Exception as e:
        st.error(f"Erreur lors du chargement des clients : {e}")

# Page des chambres disponibles
elif choix == "🛏️ Chambres Disponibles":
    st.header("Recherche de Chambres Disponibles")
    
    # Sélection des dates
    col1, col2 = st.columns(2)
    with col1:
        date_debut = st.date_input("📅 Date d'arrivée", value=date.today())
    with col2:
        date_fin = st.date_input("📅 Date de départ", value=date.today())
    
    if date_debut >= date_fin:
        st.error("La date de départ doit être postérieure à la date d'arrivée.")
    else:
        if st.button("🔍 Rechercher", type="primary"):
            try:
                query = """
                SELECT 
                    ch.id_chambre,
                    ch.numero_chambre,
                    ch.etage,
                    CASE WHEN ch.balcon = 1 THEN 'Oui' ELSE 'Non' END as balcon,
                    tc.nom_type,
                    tc.prix,
                    h.ville as ville_hotel
                FROM Chambre ch
                JOIN Type_Chambre tc ON ch.id_type = tc.id_type
                JOIN Hotel h ON ch.id_hotel = h.id_hotel
                WHERE ch.id_chambre NOT IN (
                    SELECT rc.id_chambre 
                    FROM Reservation r
                    JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
                    WHERE NOT (r.date_depart <= ? OR r.date_arrivee >= ?)
                )
                ORDER BY h.ville, ch.numero_chambre
                """
                
                df = pd.read_sql_query(query, conn, params=(str(date_debut), str(date_fin)))
                
                if not df.empty:
                    # Formatage des colonnes
                    df.columns = ['ID', 'N° Chambre', 'Étage', 'Balcon', 'Type', 'Prix/nuit (€)', 'Ville']
                    
                    st.success(f"🎉 {len(df)} chambre(s) disponible(s) du {date_debut} au {date_fin}")
                    st.dataframe(df, use_container_width=True)
                    
                    # Statistiques
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write("**Par type de chambre :**")
                        type_counts = df['Type'].value_counts()
                        st.write(type_counts)
                    with col2:
                        st.write("**Par ville :**")
                        ville_counts = df['Ville'].value_counts()
                        st.write(ville_counts)
                else:
                    st.warning("😔 Aucune chambre disponible pour cette période.")
                    
            except Exception as e:
                st.error(f"Erreur lors de la recherche : {e}")

# Page d'ajout de client
elif choix == "➕ Ajouter Client":
    st.header("Ajouter un Nouveau Client")
    
    with st.form("form_client"):
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("👤 Nom complet *", placeholder="Ex: Jean Dupont")
            adresse = st.text_input("🏠 Adresse *", placeholder="Ex: 12 Rue de la Paix")
            ville = st.text_input("🌆 Ville *", placeholder="Ex: Paris")
        
        with col2:
            code_postal = st.number_input("📮 Code postal *", min_value=1000, max_value=99999, value=75001)
            email = st.text_input("📧 Email *", placeholder="Ex: jean.dupont@email.fr")
            telephone = st.text_input("📞 Téléphone", placeholder="Ex: 0123456789")
        
        submitted = st.form_submit_button("💾 Enregistrer le client", type="primary")
        
        if submitted:
            # Validation des champs obligatoires
            if not all([nom, adresse, ville, email]):
                st.error("⚠️ Veuillez remplir tous les champs obligatoires (*).")
            else:
                try:
                    cur = conn.cursor()
                    cur.execute("""
                        INSERT INTO Client (adresse, ville, code_postal, email, telephone, nom_client) 
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (adresse, ville, code_postal, email, telephone, nom))
                    conn.commit()
                    st.success(f"✅ Client '{nom}' ajouté avec succès!")
                    
                    # Afficher les informations du client ajouté
                    st.info(f"**Détails :** {nom} - {ville} ({code_postal}) - {email}")
                    
                except Exception as e:
                    st.error(f"❌ Erreur lors de l'ajout : {e}")

# Page d'ajout de réservation
elif choix == "📝 Ajouter Réservation":
    st.header("Créer une Nouvelle Réservation")
    
    # Récupération des clients
    try:
        clients_df = pd.read_sql_query("SELECT id_client, nom_client FROM Client ORDER BY nom_client", conn)
        clients_dict = dict(zip(clients_df['nom_client'], clients_df['id_client']))
        
        with st.form("form_reservation"):
            col1, col2 = st.columns(2)
            
            with col1:
                client_nom = st.selectbox("👤 Sélectionner un client *", list(clients_dict.keys()))
                date_arrivee = st.date_input("📅 Date d'arrivée *", value=date.today())
            
            with col2:
                date_depart = st.date_input("📅 Date de départ *", value=date.today())
                
            # Sélection de chambre (optionnel pour cette version simplifiée)
            st.info("💡 La chambre sera attribuée automatiquement selon la disponibilité.")
            
            submitted = st.form_submit_button("📝 Créer la réservation", type="primary")
            
            if submitted:
                if date_arrivee >= date_depart:
                    st.error("⚠️ La date de départ doit être postérieure à la date d'arrivée.")
                else:
                    try:
                        id_client = clients_dict[client_nom]
                        cur = conn.cursor()
                        
                        # Insérer la réservation
                        cur.execute("""
                            INSERT INTO Reservation (date_arrivee, date_depart, id_client) 
                            VALUES (?, ?, ?)
                        """, (str(date_arrivee), str(date_depart), id_client))
                        
                        # Récupérer l'ID de la réservation créée
                        reservation_id = cur.lastrowid
                        
                        # Trouver une chambre disponible
                        cur.execute("""
                            SELECT id_chambre FROM Chambre 
                            WHERE id_chambre NOT IN (
                                SELECT rc.id_chambre 
                                FROM Reservation r
                                JOIN Reservation_Chambre rc ON r.id_reservation = rc.id_reservation
                                WHERE NOT (r.date_depart <= ? OR r.date_arrivee >= ?)
                            )
                            LIMIT 1
                        """, (str(date_arrivee), str(date_depart)))
                        
                        chambre_dispo = cur.fetchone()
                        
                        if chambre_dispo:
                            # Associer la chambre à la réservation
                            cur.execute("""
                                INSERT INTO Reservation_Chambre (id_reservation, id_chambre) 
                                VALUES (?, ?)
                            """, (reservation_id, chambre_dispo[0]))
                            
                            conn.commit()
                            st.success(f"✅ Réservation créée avec succès!")
                            st.info(f"**Détails :** Réservation n°{reservation_id} pour {client_nom} du {date_arrivee} au {date_depart}")
                        else:
                            # Supprimer la réservation si aucune chambre disponible
                            cur.execute("DELETE FROM Reservation WHERE id_reservation = ?", (reservation_id,))
                            conn.commit()
                            st.error("😔 Aucune chambre disponible pour cette période.")
                            
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la création : {e}")
                        
    except Exception as e:
        st.error(f"Erreur lors du chargement des clients : {e}")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("**Projet BD 2025**")
st.sidebar.markdown("*Licence IAP S4*")
st.sidebar.markdown("*réalisé par:*")
st.sidebar.markdown("*Salima Ouassas*")
st.sidebar.markdown("*et Nourelhouda Elkasra*")