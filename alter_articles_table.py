#!/usr/bin/env python
"""
Script pour ajouter les nouvelles colonnes à la table articles via SQL ALTER TABLE.
"""

import os
import sys
from sqlalchemy import text

# Ajout du chemin racine au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import de la session SQLAlchemy
from core.syntinel.db.session import engine

def alter_articles_table():
    """Ajoute les nouvelles colonnes à la table articles."""
    print("Ajout des nouvelles colonnes à la table articles...")
    
    # Créer une connexion
    with engine.begin() as connection:
        # Vérifier si les colonnes existent déjà
        for column_info in [
            {"name": "external_id", "type": "VARCHAR", "description": "ID externe de l'article"},
            {"name": "internal_url", "type": "VARCHAR", "description": "URL interne sur CryptoPanic"},
            {"name": "time_ago", "type": "VARCHAR", "description": "Âge relatif de l'article"}
        ]:
            column_name = column_info["name"]
            column_type = column_info["type"]
            description = column_info["description"]
            
            # Vérifier si la colonne existe
            result = connection.execute(text(
                f"SELECT column_name FROM information_schema.columns "
                f"WHERE table_name = 'articles' AND column_name = '{column_name}';"
            ))
            
            if result.fetchone() is None:
                print(f"Ajout de la colonne {column_name} ({description})...")
                # Ajouter la colonne
                connection.execute(text(
                    f"ALTER TABLE articles ADD COLUMN {column_name} {column_type};"
                ))
                print(f"Colonne {column_name} ajoutée avec succès.")
            else:
                print(f"La colonne {column_name} existe déjà.")
    
    print("Mise à jour de la table articles terminée.")

if __name__ == "__main__":
    # Vérifier la connectivité à la base de données
    print(f"Connexion à la base de données: {engine.url}")
    try:
        connection = engine.connect()
        connection.close()
        print("Connexion à la base de données réussie")
    except Exception as e:
        print(f"Erreur de connexion à la base de données: {e}")
        sys.exit(1)
    
    # Exécuter les ALTER TABLE
    alter_articles_table()
