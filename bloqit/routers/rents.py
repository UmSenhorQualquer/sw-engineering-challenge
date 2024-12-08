from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models.rent import Rent, RentStatus

router = APIRouter(
    prefix="/rents",
    tags=["rents"]
)

@router.get("/", response_model=List[Rent])
def get_rents(session: Session = Depends(get_session)):
    rents = session.exec(select(Rent)).all()
    return rents

@router.get("/{rent_id}", response_model=Rent)
def get_rent(rent_id: str, session: Session = Depends(get_session)):
    rent = session.get(Rent, rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")
    return rent

@router.post("/", response_model=Rent)
def create_rent(rent: Rent, session: Session = Depends(get_session)):
    session.add(rent)
    session.commit()
    session.refresh(rent)
    return rent

@router.put("/{rent_id}/status", response_model=Rent)
def update_rent_status(
    rent_id: str, status: RentStatus, session: Session = Depends(get_session)
):
    rent = session.get(Rent, rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")
    rent.status = status
    session.commit()
    session.refresh(rent)
    return rent 