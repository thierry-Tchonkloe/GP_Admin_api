#!/usr/bin/env python3
"""
Script pour recréer complètement la base de données avec les nouvelles structures
"""

import os
from app.database import engine, Base
from app.models.models import Employe, Presence, Empreinte

def main():
    print("🗑️  Suppression de l'ancienne base de données...")
    
    # Supprimer l'ancienne base de données
    if os.path.exists("gpadmin.db"):
        os.remove("gpadmin.db")
        print("✅ Ancienne base de données supprimée")
    
    print("🔄 Création de la nouvelle base de données...")
    
    # Créer toutes les nouvelles tables
    Base.metadata.create_all(bind=engine)
    
    print("✅ Base de données recréée avec succès!")
    print("📋 Nouvelles tables créées:")
    print("- employes (avec les nouveaux champs)")
    print("- empreintes (nouvelle table)")
    print("- presences (avec les nouveaux champs: employee_code, date_presence, etc.)")
    
    print("\n⚠️  ATTENTION: Toutes les données existantes ont été supprimées!")
    print("   Vous devrez recréer vos employés de test.")

if __name__ == "__main__":
    main() 