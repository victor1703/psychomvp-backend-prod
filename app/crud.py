from sqlalchemy.orm import Session
from sqlalchemy import select
from datetime import datetime
from typing import Optional, List
from app import models

# Users
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.execute(select(models.User).where(models.User.email == email)).scalar_one_or_none()

def create_user(db: Session, *, email: str, full_name: str, hashed_password: str, role: str) -> models.User:
    user = models.User(email=email, full_name=full_name, hashed_password=hashed_password, role=role)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# Availability
def create_availability(db: Session, *, psychologist_id: int, start: datetime, end: datetime, note: str | None) -> models.Availability:
    av = models.Availability(psychologist_id=psychologist_id, start_time=start, end_time=end, note=note)
    db.add(av)
    db.commit()
    db.refresh(av)
    return av

def list_availability(db: Session, *, psychologist_id: int, date_from: datetime | None = None, date_to: datetime | None = None) -> List[models.Availability]:
    stmt = select(models.Availability).where(models.Availability.psychologist_id == psychologist_id)
    if date_from:
        stmt = stmt.where(models.Availability.start_time >= date_from)
    if date_to:
        stmt = stmt.where(models.Availability.start_time < date_to)
    stmt = stmt.order_by(models.Availability.start_time.asc())
    return list(db.execute(stmt).scalars())

# Appointments
def create_appointment(db: Session, *, psychologist_id: int, patient_id: int | None, start: datetime, end: datetime) -> models.Appointment:
    ap = models.Appointment(psychologist_id=psychologist_id, patient_id=patient_id, start_time=start, end_time=end, status="booked")
    db.add(ap)
    db.commit()
    db.refresh(ap)
    return ap

def get_appointment(db: Session, appointment_id: int) -> Optional[models.Appointment]:
    return db.get(models.Appointment, appointment_id)

def list_appointments_for_psychologist(db: Session, *, psychologist_id: int, date_from: datetime | None = None, date_to: datetime | None = None) -> List[models.Appointment]:
    stmt = select(models.Appointment).where(models.Appointment.psychologist_id == psychologist_id)
    if date_from:
        stmt = stmt.where(models.Appointment.start_time >= date_from)
    if date_to:
        stmt = stmt.where(models.Appointment.start_time < date_to)
    stmt = stmt.order_by(models.Appointment.start_time.asc())
    return list(db.execute(stmt).scalars())

def reschedule_appointment(db: Session, *, appointment: models.Appointment, new_start: datetime, new_end: datetime) -> models.Appointment:
    appointment.start_time = new_start
    appointment.end_time = new_end
    appointment.status = "rescheduled"
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
