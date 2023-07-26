from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charity_project import charity_project_crud
from app.models import CharityProject


async def check_name_duplicate(
        project_name: str,
        session: AsyncSession,
) -> None:
    project_id = await charity_project_crud.get_project_id_by_name(
        project_name, session)
    if project_id is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Проект с таким именем уже существует!',
        )


async def check_project_exists(
        project_id: int,
        session: AsyncSession,
) -> CharityProject:
    project = await charity_project_crud.get(project_id, session)
    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Проект не найден!'
        )
    return project


async def check_project_before_edit(
        project_id: int,
        session: AsyncSession,
        full_amount: Optional[int] = None
) -> None:
    invested = await charity_project_crud.get_invested_by_id(project_id,
                                                             session)
    fully_invested = await charity_project_crud.get_fully_invested_by_id(
        project_id, session)
    if fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Закрытый проект нельзя редактировать!',
        )
    if full_amount:
        if invested > full_amount:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail='Требуемая сумма должна быть не менее уже внесенной',
            )


async def check_project_before_delete(
        project_id: int,
        session: AsyncSession,
) -> None:
    invested = await charity_project_crud.get_invested_by_id(project_id,
                                                             session)
    fully_invested = await charity_project_crud.get_fully_invested_by_id(
        project_id, session)
    if fully_invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
    if invested:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='В проект были внесены средства, не подлежит удалению!',
        )
