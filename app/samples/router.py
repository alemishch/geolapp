from fastapi import APIRouter, Depends
from app.samples.dao import SampleDAO
from app.samples.schemas import SSample, SSampleAdd
from app.samples.rb import RBSample
from app.drill_hole.dao import DrillHoleDAO
from typing import Union, List


router = APIRouter(prefix='/samples', tags=['Работа с образцами'])

async def verify_drill_hole(sample: SSampleAdd):
    drill_hole = await DrillHoleDAO.find_one_or_none_by_id(sample.drill_hole_id)
    if not drill_hole:
        raise HTTPException(status_code=404, detail="Скважина не найдена")
    return drill_hole


@router.post("/add/", response_model=RBSample, summary="Добавить образец")
async def add_sample(sample: SSampleAdd, drill_hole=Depends(verify_drill_hole)):
    try:
        new_sample = await SampleDAO.add(**sample.dict())
        if new_sample:
            return {"message": "Образец успешно добавлен!", "sample": new_sample}
        else:
            raise HTTPException(status_code=400, detail="Ошибка при добавлении образца!")
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера")

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
        raise HTTPException(status_code=404, detail="Образец не найден по ID")
    return sample


