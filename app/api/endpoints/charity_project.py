from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charity_project import charity_project_crud
from app.models import Donation
from app.schemas.charity_project import (CharityProjectCreate,
                                         CharityProjectDB,
                                         CharityProjectUpdate)
from app.services.sharing import share_donations
from .validators import (check_name_duplicate, check_project_before_delete,
                         check_project_before_edit, check_project_exists)

router = APIRouter()


@router.post(
    '/',
    response_model=CharityProjectDB,
    response_model_exclude_none=True,
    dependencies=[Depends(current_superuser)]
)
async def create_new_charity_project(
        project: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Создаёт благотворительный проект.
    """
    await check_name_duplicate(project.name, session)
    new_project = await charity_project_crud.create(project, session)
    return await share_donations(new_project, Donation, session)


@router.get(
    '/',
    response_model=List[CharityProjectDB],
    response_model_exclude={'close_date'}
)
async def get_all_projects(
        session: AsyncSession = Depends(get_async_session),
):
    """Возвращает список всех проектов."""
    return await charity_project_crud.get_multi(session)


@router.patch(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def partially_update_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Закрытый проект нельзя редактировать;
    нельзя установить требуемую сумму меньше уже вложенной.
    """
    project = await check_project_exists(
        project_id, session
    )
    if obj_in.name is not None:
        await check_name_duplicate(obj_in.name, session)
    if obj_in.full_amount is not None:
        await check_project_before_edit(project_id, session,
                                        obj_in.full_amount)
    else:
        await check_project_before_edit(project_id, session)
    project = await charity_project_crud.update(
        project, obj_in, session
    )
    return project


@router.delete(
    '/{project_id}',
    response_model=CharityProjectDB,
    dependencies=[Depends(current_superuser)]
)
async def remove_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """
    Только для суперюзеров.
    Удаляет проект. Нельзя удалить проект,
    в который уже были инвестированы средства, его можно только закрыть.
    """
    project = await check_project_exists(project_id, session)
    await check_project_before_delete(project_id, session)
    return await charity_project_crud.remove(project, session)
