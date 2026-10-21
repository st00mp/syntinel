#!/usr/bin/env python
"""
Script pour vérifier le contenu de la table articles après la migration.
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
    print("Vérification du contenu de la table articles...")
    
    # Créer une session
    db = SessionLocal()
    
    try:
        # Récupérer tous les articles
        articles = db.query(Article).all()
        
        if not articles:
            print("Aucun article trouvé dans la base de données.")
            return
        
        print(f"\n{len(articles)} articles trouvés dans la base de données:")
        
        for i, article in enumerate(articles, 1):
            print(f"\n--- Article {i} ---")
            article_data = {
                "id": article.id,
                "external_id": article.external_id,
                "title": article.title,
                "url": article.url,
                "internal_url": article.internal_url,
                "source": article.source,
                "time_ago": article.time_ago,
                "content_preview": article.content[:100] + "..." if article.content else None,
            }
            pprint(article_data)
    
    finally:
        db.close()

if __name__ == "__main__":
    check_articles()
