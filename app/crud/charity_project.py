from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.charity_project import CharityProject


class CRUDCharityProject(CRUDBase):
    async def get_project_id_by_name(
            self,
            project_name: str,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_id = await session.execute(select(CharityProject.id).where(
            CharityProject.name == project_name))
        return db_project_id.scalars().first()

    async def get_invested_by_id(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[int]:
        db_project_invested = await session.execute(
            select(CharityProject.invested_amount).where(
                CharityProject.id == project_id))
        return db_project_invested.scalars().first()

    async def get_fully_invested_by_id(
            self,
            project_id: int,
            session: AsyncSession,
    ) -> Optional[bool]:
        db_project_fully_invested = await session.execute(
            select(CharityProject.fully_invested).where(
                CharityProject.id == project_id))
        return db_project_fully_invested.scalars().first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        query = select(
            CharityProject.name,
            CharityProject.close_date,
            CharityProject.create_date,
            CharityProject.description
        ).where(CharityProject.fully_invested == True)
        db_objs = await session.execute(query)
        return db_objs.mappings().all()


charity_project_crud = CRUDCharityProject(CharityProject)
