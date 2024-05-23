# app/routers/appointments.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
# import stripe

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)

@router.post("/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = crud.create_appointment(db=db, appointment=appointment)
    
    # payment_intent = stripe.PaymentIntent.create(
    #     amount=5000,  # Example amount in cents
    #     currency='usd',
    #     payment_method_types=['card'],
    # )
    # db_appointment.payment_link = payment_intent.client_secret
    # db.commit()
    # db.refresh(db_appointment)
    return db_appointment

@router.get("/patient/{patient_id}", response_model=list[schemas.Appointment])
def list_appointments_for_patient(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_for_patient(db=db, patient_id=patient_id)
