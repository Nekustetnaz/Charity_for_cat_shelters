from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, PositiveInt, root_validator, validator


class CharityProjectBase(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, min_length=1)
    full_amount: Optional[PositiveInt]


class CharityProjectCreate(CharityProjectBase):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: PositiveInt


class CharityProjectDB(CharityProjectCreate):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime
    close_date: Optional[datetime]

    class Config:
        orm_mode = True


class CharityProjectUpdate(CharityProjectBase):
    invested_amount: Optional[PositiveInt]

    @validator('name')
    def name_is_not_none(cls, value: str):
        if value is None:
            raise ValueError('Имя не может быть пустым')
        return value

    @validator('invested_amount')
    def invested_amount_is_none(cls, value: str):
        if value is not None:
            raise ValueError('Нельзя изменять внесенную сумму')
        return value

    @root_validator(skip_on_failure=True)
    def values_are_not_none(cls, values):
        for value in values:
            if values[value]:
                return values
        raise ValueError('Не указаны изменяемые поля')
