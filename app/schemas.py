from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional, Literal

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserBase(BaseModel):
    email: EmailStr
    full_name: str

class UserCreate(UserBase):
    password: str = Field(min_length=6)
    role: Literal["psychologist", "patient"]

class UserOut(UserBase):
    id: int
    role: str
    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class AvailabilityCreate(BaseModel):
    start_time: datetime
    end_time: datetime
    note: Optional[str] = None

class AvailabilityOut(AvailabilityCreate):
    id: int
    psychologist_id: int
    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    psychologist_id: int
    start_time: datetime
    end_time: datetime
    patient_full_name: Optional[str] = None
    patient_email: Optional[EmailStr] = None

class AppointmentOut(BaseModel):
    id: int
    psychologist_id: int
    patient_id: Optional[int]
    start_time: datetime
    end_time: datetime
    status: str
    class Config:
        from_attributes = True

class RescheduleRequest(BaseModel):
    new_start_time: datetime
    new_end_time: datetime
