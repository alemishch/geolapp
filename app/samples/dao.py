from fastapi import APIRouter 
from sqlalchemy import select 
from app.database import async_session_maker 
from app.samples.models import Sample


router = APIRouter(prefix='/samples', tags=['Работа с образцами'])


@router.get("/", summary="Получить все образцы")
async def get_all_samples():
    async with async_session_maker() as session: 
        query = select(Sample)
        result = await session.execute(query)
        samples = result.scalars().all()
        return samples