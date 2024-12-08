from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from ..database import get_session
from ..models.bloq import Bloq

router = APIRouter(
    prefix="/bloqs",
    tags=["bloqs"]
)

@router.get("/", response_model=List[Bloq])
def get_bloqs(session: Session = Depends(get_session)):
    bloqs = session.exec(select(Bloq)).all()
    return bloqs

@router.get("/{bloq_id}", response_model=Bloq)
def get_bloq(bloq_id: str, session: Session = Depends(get_session)):
    bloq = session.get(Bloq, bloq_id)
    if not bloq:
        raise HTTPException(status_code=404, detail="Bloq not found")
    return bloq

@router.post("/", response_model=Bloq)
def create_bloq(bloq: Bloq, session: Session = Depends(get_session)):
    session.add(bloq)
    session.commit()
    session.refresh(bloq)
    return bloq 