from sqlalchemy import Column, String, Date, Boolean, Text, ForeignKey, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from app.database import Base
from datetime import datetime

# class Employe(Base):
#     __tablename__ = "employes"

#     id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
#     company_id = Column(UUID(as_uuid=True), ForeignKey("company.id"), nullable=False)
#     full_name = Column(String, nullable=False)
#     email = Column(String, unique=True, nullable=False)
#     telephone = Column(String, nullable=True)
#     poste = Column(String, nullable=True)
#     date_recrutement = Column(Date, nullable=True)
#     salaire = Column(Numeric, nullable=True)
#     code_unique = Column(String, unique=True, nullable=False)
#     empreinte_1 = Column(Text, nullable=False)
#     empreinte_2 = Column(Text, nullable=False)
#     empreinte_3 = Column(Text, nullable=False)
#     actif = Column(Boolean, default=True)
#     created_at = Column(DateTime(timezone=True), server_default=func.now())


class Employe(Base):
    __tablename__ = "employes"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    company_id = Column(String, default = "e0ce87c8-73aa-4396-9dd5-2e078b3a9722", nullable=True)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=True)
    date_of_birth = Column(Date, nullable=True)
    address = Column(String, nullable=True)
    gender = Column(String, nullable=True)
    marital_status = Column(String, nullable=True)

#    emergency_contact_name = Column(String, nullable=True)
#    emergency_contact_phone = Column(String, nullable=True)
#    emergency_contact_relation = Column(String, nullable=True)

    employee_code = Column(String, unique=True, nullable=True)
    code_unique = Column(String, unique=True, nullable=False)
    position = Column(String, nullable=True)
    department = Column(String, nullable=True)
    hire_date = Column(Date, nullable=True)
    contract_type = Column(String, nullable=True)
    salary = Column(Numeric, nullable=True)
    contract_end_date = Column(Date, nullable=True)
    work_start_time = Column(String, nullable=True)
    work_end_time = Column(String, nullable=True)

    education_level = Column(String, nullable=True)
    experience = Column(String, nullable=True)
#    skills = Column(String, nullable=True)

    skip_biometric = Column(Boolean, default=False, nullable=True)
    fingerprints_enrolled = Column(Boolean, default=False, nullable=True)

    actif = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    presences = relationship("Presence", back_populates="employe")


class Presence(Base):
    __tablename__ = "presences"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    employe_id = Column(String, ForeignKey("employes.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)

    # employe = relationship("Employe")
    employe = relationship("Employe", back_populates="presences", cascade="all, delete")

# class Company(Base):
#     __tablename__ = "company"
#     id = Column(UUID(as_uuid=True), primary_key=True,)
