from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_session
from ..models.rent import Rent, RentStatus

router = APIRouter(
    prefix="/rents",
    tags=["rents"]
)

@router.get("/", response_model=List[Rent])
async def get_rents(session: AsyncSession = Depends(get_session)):
    rents = await session.execute(select(Rent))
    return rents.scalars().all()

@router.get("/{rent_id}", response_model=Rent)
async def get_rent(rent_id: str, session: AsyncSession = Depends(get_session)):
    rent = await session.get(Rent, rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")
    return rent

@router.post("/", response_model=Rent)
async def create_rent(rent: Rent, session: AsyncSession = Depends(get_session)):
    session.add(rent)
    await session.commit()
    await session.refresh(rent)
    return rent

@router.put("/{rent_id}/status", response_model=Rent)
async def update_rent_status(
    rent_id: str, status: RentStatus, session: AsyncSession = Depends(get_session)
):
    rent = await session.get(Rent, rent_id)
    if not rent:
        raise HTTPException(status_code=404, detail="Rent not found")
    rent.status = status
    await session.commit()
    await session.refresh(rent)
    return rent 