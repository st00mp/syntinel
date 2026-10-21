#!/usr/bin/env python
"""
Script pour mettre à jour le schéma de la base de données.
Crée ou met à jour les tables selon les modèles définis dans core.syntinel.db.
"""

import os
import sys
from sqlalchemy import inspect

# Ajout du chemin racine au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import des modèles et de la configuration DB
from core.syntinel.db.session import engine, Base, SessionLocal
from core.syntinel.db.models import Article, Draft

def update_schema():
    """Met à jour le schéma de la base de données selon les modèles."""
    print("Mise à jour du schéma de la base de données...")
    
    # Créer une connexion
    connection = engine.connect()
    
    # Obtenir l'inspecteur SQLAlchemy
    inspector = inspect(engine)
    
    # Vérifier si la table articles existe
    tables = inspector.get_table_names()
    if 'articles' in tables:
        print("Table 'articles' trouvée dans la base de données")
        
        # Liste des colonnes actuelles
        columns = [col['name'] for col in inspector.get_columns('articles')]
        print(f"Colonnes actuelles: {columns}")
        
        # Liste des nouvelles colonnes attendues
        model_columns = [column.key for column in Article.__table__.columns]
        print(f"Colonnes du modèle: {model_columns}")
        
        # Identifier les colonnes manquantes
        missing_columns = [col for col in model_columns if col not in columns]
        if missing_columns:
            print(f"Colonnes à ajouter: {missing_columns}")
            print("Attention: Les colonnes manquantes nécessitent une migration.")
            print("Nous allons tenter de mettre à jour le schéma...")
    else:
        print("Table 'articles' non trouvée dans la base de données")
    
    # Créer/mettre à jour toutes les tables
    Base.metadata.create_all(engine, checkfirst=True)
    print("Mise à jour du schéma terminée")
    
    # Fermer la connexion
    connection.close()

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
    
    # Mettre à jour le schéma
    update_schema()
