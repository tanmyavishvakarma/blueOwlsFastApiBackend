from fastapi import FastAPI
from app.routers import patients, appointments
from app.database import engine, Base
from app import models
from fastapi.middleware.cors import CORSMiddleware
from sqladmin import Admin, ModelView

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

admin = Admin(app, engine)
class PatientAdmin(ModelView, model=models.Patient):
    column_list = [models.Patient.id, models.Patient.name, models.Patient.mobile_no, models.Patient.appointments]
admin.add_view(PatientAdmin)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(patients.router)
app.include_router(appointments.router)
