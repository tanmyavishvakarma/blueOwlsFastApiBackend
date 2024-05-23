# app/routers/patients.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas, models
from app.database import get_db

router = APIRouter(
    prefix="/patients",
    tags=["patients"],
)

@router.post("/", response_model=schemas.Patient)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db=db, patient=patient)

@router.get("/", response_model=List[schemas.Patient])
def list_patients(db: Session = Depends(get_db)):
    return crud.get_patients(db=db)

@router.get("/search", response_model=List[schemas.Patient])
def search_patients(name: str, db: Session = Depends(get_db)):
    return db.query(models.Patient).filter(models.Patient.name.contains(name)).all()

@router.get("/{patient_id}", response_model=schemas.Patient)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient
