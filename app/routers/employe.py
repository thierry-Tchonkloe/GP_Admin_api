from fastapi import APIRouter, Depends, HTTPException, FastAPI
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.models import Employe, Presence
from app.schemas.schemas import EmployeCreate, EmployeRead, FingerprintVerificationData
from app.utils import generate_code_unique
from typing import List
from datetime import datetime
import hashlib

#from fastapi import APIRouter, Depends, HTTPException
#from sqlalchemy.orm import Session
from base64 import b64decode

#from ..models import Employe
#from ..database import get_db
#from ..schemas import FingerprintData  # si tu l'utilises



# Définition du router
router = APIRouter(prefix="/employes", tags=["Employes"])

# Dépendance à la base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Route de création d'un employé
# @router.post("/", response_model=EmployeRead)
# def create_employe(employe: EmployeCreate, db: Session = Depends(get_db)):
#     code_unique = generate_code_unique()
#     new_employe = Employe(code_unique=code_unique, **employe.dict())
#     db.add(new_employe)
#     db.commit()
#     db.refresh(new_employe)
#     return new_employe

def hash_fingerprint(fp: bytes):
    """Tu peux comparer les empreintes via un hash simplifié"""
    return hashlib.sha256(fp).hexdigest()


@router.post("/", response_model=EmployeRead)
def create_employe(employe: EmployeCreate, db: Session = Depends(get_db)):
    code_unique = generate_code_unique(db)  # ✅ ici on passe db
    new_employe = Employe(code_unique=code_unique, **employe.dict())
    db.add(new_employe)
    db.commit()
    db.refresh(new_employe)
    return new_employe


@router.get("/", response_model=List[EmployeRead])
def get_all_employes(db: Session = Depends(get_db)):
    employes = db.query(Employe).all()
    return employes


@router.get("/verify-code/{code_unique}")
def verify_code_unique(code_unique: int, db: Session = Depends(get_db)):
    employe = db.query(Employe).filter(Employe.code_unique == code_unique).first()

    if not employe:
        return {"status": "error", "message": "Code Invalide"}

    if employe.fingerprints_enrolled < 2:
        return {
            "status": "enrollment_required",
            "message": "enrolled again",
            "employe_id": str(employe.id),
            "full_name": employe.full_name
        }

    return {
        "status": "pointage",
        "message": "rady for pointage.",
        "employe_id": str(employe.id),
        "full_name": employe.full_name
    }


#router = APIRouter(prefix="/empreintes", tags=["Empreintes"])

# @router.post("/enregistrer/")
# def enregistrer_empreintes(data: FingerprintData, db: Session = Depends(get_db)):
#     employe = db.query(Employe).filter(Employe.code_unique == data.code_unique).first()
    
#     if not employe:
#         raise HTTPException(status_code=404, detail="Employé non trouvé")

#     try:
#         if data.fingerprint_1:
#             employe.fingerprint_1 = b64decode(data.fingerprint_1)
#         if data.fingerprint_2:
#             employe.fingerprint_2 = b64decode(data.fingerprint_2)

#         db.commit()
#         return {"message": "Empreintes enregistrées avec succès"}
    
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Erreur d’enregistrement : {str(e)}")


@router.post("/verifier-ou-enregistrer/")
def verifier_ou_enregistrer(data: FingerprintVerificationData, db: Session = Depends(get_db)):
    employe = db.query(Employe).filter(Employe.code_unique == data.code_unique).first()

    if not employe:
        raise HTTPException(status_code=404, detail="Employé non trouvé")

    # Conversion fingerprint reçue
    nouvelle_fp = b64decode(data.fingerprint)

    # Cas 1 : les empreintes ne sont pas encore enregistrées
    if not employe.fingerprint_1 or not employe.fingerprint_2:
        # Enregistre comme première ou deuxième empreinte
        if not employe.fingerprint_1:
            employe.fingerprint_1 = nouvelle_fp
        elif not employe.fingerprint_2:
            employe.fingerprint_2 = nouvelle_fp
        else:
            raise HTTPException(status_code=400, detail="Les deux empreintes sont déjà enregistrées")

        db.commit()
        return {"message": "Empreinte enregistrée avec succès"}

    # Cas 2 : les deux empreintes sont déjà présentes, on vérifie la correspondance
    fp1_hash = hash_fingerprint(employe.fingerprint_1)
    fp2_hash = hash_fingerprint(employe.fingerprint_2)
    new_fp_hash = hash_fingerprint(nouvelle_fp)

    if new_fp_hash in [fp1_hash, fp2_hash]:
        # Créer une ligne de présence
        presence = Presence(employe_id=employe.id, timestamp=datetime.now())
        db.add(presence)
        db.commit()
        return {"message": "Présence enregistrée", "nom": employe.full_name}

    else:
        raise HTTPException(status_code=401, detail="Empreinte non reconnue")
