from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    full_name = Column(String(255), nullable=False)
    hashed_password = Column(String(255), nullable=False)
    role = Column(String(32), nullable=False)  # "psychologist" | "patient"
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    availabilities = relationship("Availability", back_populates="psychologist", cascade="all, delete-orphan")
    appointments_as_psy = relationship("Appointment", back_populates="psychologist", foreign_keys="Appointment.psychologist_id")
    appointments_as_patient = relationship("Appointment", back_populates="patient", foreign_keys="Appointment.patient_id")

class Availability(Base):
    __tablename__ = "availabilities"
    id = Column(Integer, primary_key=True)
    psychologist_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    note = Column(String(255), nullable=True)

    psychologist = relationship("User", back_populates="availabilities")

    __table_args__ = (
        UniqueConstraint("psychologist_id", "start_time", name="uq_psy_start"),
    )

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True)
    psychologist_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    patient_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    start_time = Column(DateTime, nullable=False, index=True)
    end_time = Column(DateTime, nullable=False)
    status = Column(String(32), default="booked", nullable=False)  # booked | rescheduled | cancelled
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    psychologist = relationship("User", foreign_keys=[psychologist_id], back_populates="appointments_as_psy")
    patient = relationship("User", foreign_keys=[patient_id], back_populates="appointments_as_patient")

    __table_args__ = (
        UniqueConstraint("psychologist_id", "start_time", name="uq_psy_appt_start"),
    )
