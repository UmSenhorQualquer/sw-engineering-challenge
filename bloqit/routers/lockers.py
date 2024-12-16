from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from ..database import get_session
from ..models.locker import Locker, LockerStatus

router = APIRouter(
    prefix="/lockers",
    tags=["lockers"]
)

@router.get("/", response_model=List[Locker])
async def get_lockers(session: AsyncSession = Depends(get_session)):
    lockers = await session.execute(select(Locker))
    return lockers.scalars().all()

@router.get("/{locker_id}", response_model=Locker)
async def get_locker(locker_id: str, session: AsyncSession = Depends(get_session)):
    locker = await session.get(Locker, locker_id)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    return locker

@router.post("/", response_model=Locker)
async def create_locker(locker: Locker, session: AsyncSession = Depends(get_session)):
    session.add(locker)
    await session.commit()
    await session.refresh(locker)
    return locker

@router.put("/{locker_id}/status", response_model=Locker)
async def update_locker_status(
    locker_id: str, status: LockerStatus, session: AsyncSession = Depends(get_session)
):
    locker = await session.get(Locker, locker_id)
    if not locker:
        raise HTTPException(status_code=404, detail="Locker not found")
    locker.status = status
    await session.commit()
    await session.refresh(locker)
    return locker 