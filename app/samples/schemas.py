from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, Field, ConfigDict

class SSample(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_name: str = Field(..., description="Название")
    drill_hole_id: int = Field(..., description="id скважины")
    depth_m: Optional[float] = Field(None, description="Глубина")
    rock_type: Optional[str] = Field(None, description="Type of rock")
    code: Optional[str] = Field(None, description="Sample code")
    full_name: Optional[str] = Field(None, description="Full name of the sample")
    texture: Optional[str] = Field(None, description="Texture description")
    structure: Optional[str] = Field(None, description="Structure description")
    macro_description: Optional[str] = Field(None, description="Macro description")
    micro_description: Optional[str] = Field(None, description="Micro description")
    ore_mineralization: Optional[str] = Field(None, description="Ore mineralization description")


class SSampleAdd(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    sample_name: str = Field(..., description="Unique name of the sample")
    drill_hole_id: int = Field(..., description="drill hole id")
    depth_m: Optional[float] = Field(None, description="Depth in meters")
    rock_type: Optional[str] = Field(None, description="Type of rock")
    code: Optional[str] = Field(None, description="Sample code")
    full_name: Optional[str] = Field(None, description="Full name of the sample")
    texture: Optional[str] = Field(None, description="Texture description")
    structure: Optional[str] = Field(None, description="Structure description")
    macro_description: Optional[str] = Field(None, description="Macro description")
    micro_description: Optional[str] = Field(None, description="Micro description")
    ore_mineralization: Optional[str] = Field(None, description="Ore mineralization description")
