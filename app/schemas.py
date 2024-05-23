# app/schemas.py
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class AppointmentBase(BaseModel):
    patient_id: int
    appointment_time: datetime

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    payment_link: Optional[str] = None

    class Config:
        orm_mode = True

class PatientBase(BaseModel):
    name: str
    mobile_no: str
    email: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    appointments: List[Appointment] = []

    class Config:
        orm_mode = True
