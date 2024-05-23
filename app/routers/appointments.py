
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas, models
from app.database import get_db
import stripe
import os
from dotenv import load_dotenv

load_dotenv()
stripe.api_key = os.getenv("STRIPE_API_KEY")

router = APIRouter(
    prefix="/appointments",
    tags=["appointments"],
)


# Stripe Price Object
# {
#   "active": true,
#   "billing_scheme": "per_unit",
#   "created": 1716498097,
#   "currency": "inr",
#   "custom_unit_amount": null,
#   "id": "price_1PJilZSJMwRXloFIIwimlQ3e",
#   "livemode": false,
#   "lookup_key": null,
#   "metadata": {},
#   "nickname": null,
#   "object": "price",
#   "product": "prod_QA2rKJbPTUJTc5",
#   "recurring": null,
#   "tax_behavior": "unspecified",
#   "tiers_mode": null,
#   "transform_quantity": null,
#   "type": "one_time",
#   "unit_amount": 5000,
#   "unit_amount_decimal": "5000"
# }


@router.post("/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = crud.create_appointment(db=db, appointment=appointment)

    payment_link = stripe.PaymentLink.create(
    line_items=[{"price": "price_1PJilZSJMwRXloFIIwimlQ3e", "quantity": 1}],)
    db_appointment.payment_link = payment_link.url
    db.commit()
    db.refresh(db_appointment)
    return db_appointment

@router.get("/patient/{patient_id}", response_model=list[schemas.Appointment])
def list_appointments_for_patient(patient_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_for_patient(db=db, patient_id=patient_id)
