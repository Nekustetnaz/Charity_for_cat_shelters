from typing import Tuple

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase


def _donate_calculations(new_obj_amount: int,
                         new_obj_invested: int,
                         obj_amount: int,
                         obj_invested: int) -> Tuple:
    if new_obj_amount - new_obj_invested >= obj_amount - obj_invested:
        new_obj_invested = new_obj_invested + obj_amount - obj_invested
        return new_obj_invested, obj_amount
    obj_invested = obj_invested + new_obj_amount - new_obj_invested
    return new_obj_amount, obj_invested


async def share_donations(
        new_obj,
        db_obj,
        session: AsyncSession
):
    """
    Если создан новый проект, перенаправит средства
    с существующих пожертвований на него.
    Если создано новое пожертвование, перенаправит средства
    с него на существующие проекты.
    """
    new_obj_amount = new_obj.full_amount
    new_obj_invested = new_obj.invested_amount
    db_objects = await session.execute(
        select(db_obj).where(db_obj.fully_invested.is_(False)).order_by(
            db_obj.create_date))
    for obj in db_objects.scalars().all():
        obj_amount = obj.full_amount
        obj_invested = obj.invested_amount
        new_obj_result, obj_result = _donate_calculations(new_obj_amount,
                                                          new_obj_invested,
                                                          obj_amount,
                                                          obj_invested)
        if new_obj_result == new_obj_amount:
            if obj_result == obj_amount:
                await CRUDBase(obj.__class__).update_invested_or_close(
                    obj, session
                )
            else:
                await CRUDBase(obj.__class__).update_invested_or_close(
                    obj, session, obj_result
                )
            await CRUDBase(new_obj.__class__).update_invested_or_close(
                new_obj, session
            )
            await session.commit()
            await session.refresh(new_obj)
            return new_obj
        await CRUDBase(obj.__class__).update_invested_or_close(obj, session)
        await CRUDBase(new_obj.__class__).update_invested_or_close(
            new_obj, session, new_obj_result
        )
        new_obj_invested = new_obj_result
    await session.commit()
    await session.refresh(new_obj)
    return new_obj
