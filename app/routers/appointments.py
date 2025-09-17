from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.schemas import AppointmentCreate, AppointmentOut, RescheduleRequest
from app.database import get_db
from app.deps import get_current_user
from app import crud, models
from app.emailer import send_email

router = APIRouter(prefix="/appointments", tags=["appointments"])

@router.post("/", response_model=AppointmentOut)
def create_appointment(payload: AppointmentCreate, db: Session = Depends(get_db)):
    # MVP: si no existe el paciente, lo creamos "anónimo" si viene email/nombre
    patient_id = None
    if payload.patient_email and payload.patient_full_name:
        existing = crud.get_user_by_email(db, payload.patient_email)
        if existing:
            patient_id = existing.id
        else:
            from app.security import get_password_hash
            patient = crud.create_user(
                db,
                email=payload.patient_email,
                full_name=payload.patient_full_name,
                hashed_password=get_password_hash("temp1234"),
                role="patient",
            )
            patient_id = patient.id

    try:
        ap = crud.create_appointment(
            db,
            psychologist_id=payload.psychologist_id,
            patient_id=patient_id,
            start=payload.start_time,
            end=payload.end_time,
        )
    except Exception as e:
        raise HTTPException(status_code=409, detail="Slot not available or already booked")

    psy = db.get(models.User, payload.psychologist_id)
    if psy:
        send_email(
            to=psy.email,
            subject="Nuevo turno reservado",
            body=f"{payload.patient_full_name or 'Paciente'} reservó {payload.start_time} - {payload.end_time}",
        )
    if payload.patient_email:
        send_email(
            to=payload.patient_email,
            subject="Confirmación de turno",
            body=f"Tu turno fue confirmado para {payload.start_time}.",
        )
    return ap

@router.get("/psychologist/{psychologist_id}", response_model=List[AppointmentOut])
def list_appointments(psychologist_id: int, db: Session = Depends(get_db), date_from: Optional[datetime] = None, date_to: Optional[datetime] = None, current=Depends(get_current_user)):
    if current.role != "psychologist" or current.id != psychologist_id:
        raise HTTPException(status_code=403, detail="Not allowed")
    return crud.list_appointments_for_psychologist(db, psychologist_id=psychologist_id, date_from=date_from, date_to=date_to)

@router.post("/{appointment_id}/reschedule", response_model=AppointmentOut)
def reschedule(appointment_id: int, payload: RescheduleRequest, db: Session = Depends(get_db)):
    ap = crud.get_appointment(db, appointment_id)
    if not ap:
        raise HTTPException(status_code=404, detail="Appointment not found")
    if payload.new_end_time <= payload.new_start_time:
        raise HTTPException(status_code=400, detail="Invalid times")
    try:
        ap = crud.reschedule_appointment(db, appointment=ap, new_start=payload.new_start_time, new_end=payload.new_end_time)
    except Exception:
        raise HTTPException(status_code=409, detail="New slot collides with another appointment")

    psy = db.get(models.User, ap.psychologist_id)
    if psy:
        send_email(
            to=psy.email,
            subject="Turno reprogramado",
            body=f"Se reprogramó a {ap.start_time} - {ap.end_time}",
        )
    if ap.patient and ap.patient.email:
        send_email(
            to=ap.patient.email,
            subject="Tu sesión fue reprogramada",
            body=f"Nueva fecha: {ap.start_time}",
        )
    return ap
