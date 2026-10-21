#!/usr/bin/env python
"""
Script pour afficher le contenu de la table articles avec le nouveau schéma.
"""

import os
import sys
from pprint import pprint

# Ajout du chemin racine au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

# Import des modèles et de la session
from core.syntinel.db.session import SessionLocal
from core.syntinel.db.models import Article

def check_articles():
    """Vérifie et affiche le contenu de la table articles."""
    print("Contenu de la table articles avec le nouveau schéma :")
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Récupérer tous les articles
        articles = db.query(Article).all()
        
        if not articles:
            print("Aucun article trouvé dans la base de données.")
            return
        
        print(f"\n{len(articles)} articles trouvés :\n")
        
        for article in articles:
            print(f"------ Article ID: {article.id} ------")
            print(f"article_id (CryptoPanic): {article.article_id}")
            print(f"title: {article.title}")
            print(f"internal_url: {article.internal_url}")
            print(f"canonical_url: {article.canonical_url}")
            print(f"source: {article.source}")
            print(f"published_at: {article.published_at}")
            print(f"ingestion_timestamp: {article.ingestion_timestamp}")
            
            # Afficher un aperçu du contenu
            content_preview = article.content[:100] + "..." if len(article.content) > 100 else article.content
            print(f"content: {content_preview}")
            print("\n")
    
    finally:
        db.close()

if __name__ == "__main__":
    check_articles()
