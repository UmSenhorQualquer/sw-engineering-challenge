from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models.locker import Locker, LockerStatus

router = APIRouter(
    prefix="/lockers",
    tags=["lockers"]
)

@router.get("/", response_model=List[Locker])
def get_lockers(session: Session = Depends(get_session)):
    lockers = session.exec(select(Locker)).all()
    return lockers

@router.get("/{locker_id}", response_model=Locker)
def get_locker(locker_id: str, session: Session = Depends(get_session)):
    locker = session.get(Locker, locker_id)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    return locker

@router.post("/", response_model=Locker)
def create_locker(locker: Locker, session: Session = Depends(get_session)):
    session.add(locker)
    session.commit()
    session.refresh(locker)
    return locker

@router.put("/{locker_id}/status", response_model=Locker)
def update_locker_status(
    locker_id: str, status: LockerStatus, session: Session = Depends(get_session)
):
    locker = session.get(Locker, locker_id)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    locker.status = status
    session.commit()
    session.refresh(locker)
    return locker 