#!/usr/bin/env python3
"""
Script pour mettre à jour la base de données avec les nouvelles tables
"""

from app.database import create_tables, engine
from app.models.models import Base

def main():
    print("Mise à jour de la base de données...")
    
    # Créer toutes les nouvelles tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Base de données mise à jour avec succès!")
    print("Nouvelles tables créées:")
    print("- empreintes")
    print("- presences (mise à jour)")
    print("- employes (mise à jour)")

if __name__ == "__main__":
    main() 