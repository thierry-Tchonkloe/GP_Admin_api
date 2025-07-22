from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date, datetime
import uuid

# class EmployeBase(BaseModel):
#     full_name: str
#     email: Optional[EmailStr] = None
#     telephone: Optional[str] = None
#     poste: Optional[str] = None
#     date_recrutement: date
#     salaire: Optional[float] = None
#     empreinte_1: str
#     empreinte_2: str
#     empreinte_3: str

class EmployeBase(BaseModel):
    full_name: str
    email: str
    phone: Optional[str]
    date_of_birth: Optional[date]
    address: Optional[str]
    gender: Optional[str]
    marital_status: Optional[str]

    employee_code: Optional[str]  # ✅ CORRECTION ICI
    #code_unique: str  # ✅ À AJOUTER
    position: Optional[str]
    department: Optional[str]
    hire_date: Optional[date]
    contract_type: Optional[str]
    salary: Optional[float]
    contract_end_date: Optional[str]
    work_start_time: Optional[str]
    work_end_time: Optional[str]

    education_level: Optional[str]
    experience: Optional[str]
    skip_biometric: Optional[bool]





class FingerprintVerificationData(BaseModel):
    code_unique: str
    fingerprint: str  # base64


class EmployeCreate(EmployeBase):
    pass

class EmployeRead(EmployeBase):
    id: uuid.UUID
    company_id: uuid.UUID
    code_unique: str
    actif: bool
    created_at: datetime

    class Config:
        orm_mode = True