from pydantic import BaseModel, Field, ConfigDict
from typing import Optional


class RBSample(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the sample")
    sample_name: Optional[str] = Field(None, description="Unique name of the sample")
    drill_hole_id: Optional[int] = Field(None, description="Drill hole ID")  
    depth_m: Optional[float] = Field(None, description="Depth")
    rock_type: Optional[str] = Field(None, description="Type of rock")
    code: Optional[str] = Field(None, description="Sample code")
    full_name: Optional[str] = Field(None, description="Full name of the sample")
    texture: Optional[str] = Field(None, description="Texture description")
    structure: Optional[str] = Field(None, description="Structure description")
    macro_description: Optional[str] = Field(None, description="Macro description")
    micro_description: Optional[str] = Field(None, description="Micro description")
    ore_mineralization: Optional[str] = Field(None, description="Ore mineralization description")

    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data