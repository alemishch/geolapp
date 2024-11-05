from pydantic import BaseModel, ConfigDict
from typing import Optional

class SDrillHole(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    drill_hole: str
    geological_complex: Optional[str] = None
    ore_zone: Optional[str] = None
    # Include other fields as needed
