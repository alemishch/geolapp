from fastapi import APIRouter, Depends
from app.drill_hole.dao import DrillHoleDAO
from app.drill_hole.schemas import SDrillHole
from app.drill_hole.rb import RBDrillHole
from typing import Union, List


router = APIRouter(prefix='/drill_hole', tags=['Скважины'])


@router.get("/", summary="Получить скважины")
async def get_all_drill_holes(request_body: RBDrillHole = Depends()) -> list[SDrillHole]:
    return await DrillHoleDAO.find_all(**request_body.to_dict())

@router.get("/by_filter", summary="Получить один образец по фильтру", response_model=List[SDrillHole])
async def get_drill_hole_by_filter(request_body: RBDrillHole = Depends()) -> List[SDrillHole]:
    filters = request_body.to_dict()
    drill_hole = await DrillHoleDAO.find_all(**filters)
    if drill_hole is None:
        return {'message': 'Скважина с указанными параметрами не найдена!'}
    return drill_hole    

@router.get("/{id}", summary="Получить скважину по id", response_model=SDrillHole)
async def get_drill_hole_by_id(id: int) -> SDrillHole:
    drill_hole = await DrillHoleDAO.find_one_or_none_by_id(id)
    if drill_hole is None:
        raise HTTPException(status_code=404, detail="Drill hole not found")
    return drill_hole