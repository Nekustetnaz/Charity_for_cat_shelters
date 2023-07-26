from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser, current_user
from app.crud.donation import donation_crud
from app.models import CharityProject, User
from app.schemas.donation import AllDonationDB, DonationCreate, DonationDB
from app.services.sharing import share_donations

router = APIRouter()


@router.post(
    '/',
    response_model=DonationDB,
    response_model_exclude_none=True
)
async def create_donation(
        reservation: DonationCreate,
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Сделать пожертвование."""
    new_donation = await donation_crud.create(
        reservation, session, user
    )
    return await share_donations(new_donation, CharityProject, session)


@router.get(
    '/',
    response_model=List[AllDonationDB],
    dependencies=[Depends(current_superuser)]
)
async def get_all_reservations(
        session: AsyncSession = Depends(get_async_session)
):
    """
    Только для суперюзеров.
    Возвращает список всех пожертвований.
    """
    return await donation_crud.get_multi(session)


@router.get(
    '/my',
    response_model=List[DonationDB]
)
async def get_my_donations(
        session: AsyncSession = Depends(get_async_session),
        user: User = Depends(current_user)
):
    """Вернуть список пожертвований пользователя, выполняющего запрос."""
    return await donation_crud.get_by_user(session=session, user=user)
