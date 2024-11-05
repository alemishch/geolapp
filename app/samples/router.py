from fastapi import APIRouter, Depends
from app.samples.dao import SampleDAO
from app.samples.schemas import SSample
from app.samples.rb import RBSample
from typing import Union, List


router = APIRouter(prefix='/samples', tags=['Работа с образцами'])


@router.get("/", summary="Получить все образцы")
async def get_all_samples(request_body: RBSample = Depends()) -> list[SSample]:
    return await SampleDAO.find_all(**request_body.to_dict())

@router.get("/by_filter", summary="Получить один образец по фильтру", response_model=List[SSample])
async def get_sample_by_filter(request_body: RBSample = Depends()) -> List[SSample]:
    filters = request_body.to_dict()
    sample = await SampleDAO.find_all(**filters)
    if sample is None:
        return {'message': 'Образец с указанными параметрами не найден!'}
    return sample   

@router.get("/drill_hole/{drill_hole_id}", summary="Получить образцы по drill_hole_id", response_model=List[SSample])
async def get_samples_by_drill_hole_id(drill_hole_id: int,) -> List[SSample]:
    samples = await SampleDAO.find_all(drill_hole_id=drill_hole_id)
    return samples

@router.get("/{id}", summary="Получить образец по id", response_model=SSample)
async def get_sample_by_id(id: int) -> SSample:
    sample = await SampleDAO.find_one_or_none_by_id(id)
    if sample is None:
        raise HTTPException(status_code=404, detail="Sample not found")
    return sample


