from pydantic import BaseModel, ConfigDict
from typing import Optional
from pydantic import Field

class SDrillHole(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    drill_hole: str
    geological_complex: Optional[str] = None
    ore_zone: Optional[str] = None


class SDrillHoleAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    drill_hole: str = Field(..., description="Название скважины")
    geological_complex: Optional[str] = Field(None, description="Комплекс")
    ore_zone: Optional[str] = Field(None, description="Рудная зона")