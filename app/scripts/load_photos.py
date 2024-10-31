import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import async_session_maker
from app.samples.models import Sample, Photos


async def load_photos():
    async with async_session_maker() as session:
        # Get all samples
        result = await session.execute(select(Sample))
        samples = result.scalars().all()

        for sample in samples:
            sample_name = sample.sample_name.lower()
            photos = Photos(
                sample_name=sample.sample_name,
                macro=f"img/macro/{sample_name}.jpg" if os.path.exists(f"img/macro/{sample_name}.jpg") else None,
                straight_light=f"img/straight_light/{sample_name}.jpg" if os.path.exists(f"img/straight_light/{sample_name}.jpg") else None,
                reflected_light=f"img/reflected_light/{sample_name}.jpg" if os.path.exists(f"img/reflected_light/{sample_name}.jpg") else None
            )
            session.add(photos)
        
        await session.commit()

def main():
    asyncio.run(load_photos())

if __name__ == "__main__":
    main()