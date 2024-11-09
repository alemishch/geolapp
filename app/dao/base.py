from sqlalchemy.future import select
from app.database import async_session_maker
from typing import List, Any
from sqlalchemy.orm import selectinload


class BaseDAO:
    model = None
    default_relationships = []
    
    @classmethod
    async def find_all(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=data_id)
            if cls.default_relationships:
                query = query.options(*[selectinload(rel) for rel in cls.default_relationships])
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            if cls.default_relationships:
                query = query.options(*[selectinload(rel) for rel in cls.default_relationships])
            result = await session.execute(query)
            return result.scalar_one_or_none()


    @classmethod
    async def add(cls, **values):
        async with async_session_maker() as session:
            async with session.begin():
                new_instance = cls.model(**values)
                session.add(new_instance)
                try:
                    await session.commit()
                except SQLAlchemyError as e:
                    await session.rollback()
                    raise e
                return new_instance     