from datetime import datetime
from typing import Optional

from pydantic import BaseModel, PositiveInt


class DonationCreate(BaseModel):
    full_amount: PositiveInt
    comment: Optional[str]


class DonationDB(DonationCreate):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class AllDonationDB(DonationDB):
    id: int
    create_date: datetime
    user_id: int
    invested_amount: int
    fully_invested: bool

    class Config:
        orm_mode = True
