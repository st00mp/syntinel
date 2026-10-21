#!/usr/bin/env python
"""
Script pour réinitialiser complètement la base de données et recréer les tables
selon les nouveaux modèles.
"""

import os
import sys
import time
from sqlalchemy import inspect, text

# Ajout du chemin racine au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import des modèles et de la configuration DB
from core.syntinel.db.session import engine, Base, SessionLocal
from core.syntinel.db.models import Article, Draft

def reset_database():
    """Supprime toutes les tables et les recrée avec le nouveau schéma."""
    print("Réinitialisation complète de la base de données...")
    
    # Obtenir l'inspecteur SQLAlchemy
    inspector = inspect(engine)
    
    # Obtenir toutes les tables existantes
    tables = inspector.get_table_names()
    print(f"Tables existantes: {tables}")
    
    # Supprimer toutes les tables
    with engine.begin() as connection:
        if 'articles' in tables:
            print("Suppression de la table 'articles'...")
            connection.execute(text("DROP TABLE IF EXISTS articles CASCADE;"))
        
        if 'drafts' in tables:
            print("Suppression de la table 'drafts'...")
            connection.execute(text("DROP TABLE IF EXISTS drafts CASCADE;"))
        
        # Attendre un moment pour s'assurer que les tables sont bien supprimées
        time.sleep(1)
    
    # Recréer les tables avec le nouveau schéma
    print("Création des tables avec le nouveau schéma...")
    Base.metadata.create_all(engine)
    
    # Vérifier les nouvelles tables
    inspector = inspect(engine)
    new_tables = inspector.get_table_names()
    print(f"Nouvelles tables créées: {new_tables}")
    
    # Vérifier les colonnes de la table articles
    if 'articles' in new_tables:
        columns = [col['name'] for col in inspector.get_columns('articles')]
        print(f"Colonnes de la table 'articles': {columns}")
    
    print("Réinitialisation terminée.")

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
    
    # Demander confirmation avant de réinitialiser
    confirm = input("Attention: Toutes les données existantes seront supprimées. Continuer? (o/n): ")
    if confirm.lower() != 'o':
        print("Opération annulée.")
        sys.exit(0)
    
    # Réinitialiser la base de données
    reset_database()
