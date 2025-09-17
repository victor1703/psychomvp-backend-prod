from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional
from app.schemas import AvailabilityCreate, AvailabilityOut
from app.database import get_db
from app.deps import get_current_user
from app import crud

router = APIRouter(prefix="/availability", tags=["availability"])

@router.post("/", response_model=AvailabilityOut)
def create_availability(payload: AvailabilityCreate, db: Session = Depends(get_db), current=Depends(get_current_user)):
    if current.role != "psychologist":
        raise HTTPException(status_code=403, detail="Only psychologists can create availability")
    if payload.end_time <= payload.start_time:
        raise HTTPException(status_code=400, detail="end_time must be after start_time")
    av = crud.create_availability(
        db,
        psychologist_id=current.id,
        start=payload.start_time,
        end=payload.end_time,
        note=payload.note,
    )
    return av

@router.get("/{psychologist_id}", response_model=List[AvailabilityOut])
def list_availability(psychologist_id: int, db: Session = Depends(get_db), date_from: Optional[datetime] = None, date_to: Optional[datetime] = None):
    return crud.list_availability(db, psychologist_id=psychologist_id, date_from=date_from, date_to=date_to)
