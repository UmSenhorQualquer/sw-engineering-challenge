import uuid
from .locker import Locker
from sqlmodel import Column, SQLModel, Field, Relationship, String
from typing import Optional
from enum import Enum


class RentSize(str, Enum):
    M = "M"
    L = "L"
    XL = "XL"

class RentStatus(str, Enum):
    CREATED = "CREATED"
    WAITING_PICKUP = "WAITING_PICKUP"
    WAITING_DROPOFF = "WAITING_DROPOFF"
    DELIVERED = "DELIVERED"

class Rent(SQLModel, table=True):
    id: str = Field(primary_key=True, default_factory=lambda: str(uuid.uuid4()))
    lockerId: Optional[str] = Field(default=None, foreign_key="locker.id")
    weight: float
    size: RentSize
    status: RentStatus
    
    locker: Locker | None = Relationship(back_populates="rents") 