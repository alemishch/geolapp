from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class RBDrillHole(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description = 'drill hole id')
    drill_hole: Optional[str] = Field(None, description = 'drill hole name')
    geological_complex: Optional[str] = Field(None, description = 'geological complex name')
    ore_zone: Optional[str] = Field(None, description = 'ore zone name')

    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data