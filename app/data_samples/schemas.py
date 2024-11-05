from datetime import datetime, date
from typing import Optional, List
import re
from pydantic import BaseModel, Field, ConfigDict


class SPhotos(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    macro: Optional[str] = Field(None, description="URL or path to macro photo")
    straight_light: Optional[str] = Field(None, description="URL or path to straight light photo")
    reflected_light: Optional[str] = Field(None, description="URL or path to reflected light photo")


class SMineralComposition(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    mineral_name: str = Field(..., description="Name of the mineral")
    percentage: Optional[float] = Field(None, description="Percentage composition of the mineral")
    main_secondary: Optional[str] = Field(None, description="Indicates if the mineral is main or secondary")


class SOreMineralization(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    mineral_name: str = Field(..., description="Name of the ore mineral")
    percentage: Optional[float] = Field(None, description="Percentage composition of the ore mineral")
    main_secondary: Optional[str] = Field(None, description="Indicates if the ore mineral is main or secondary")


class SVein(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    vein_name: str = Field(..., description="Name of the vein")
    percentage: Optional[float] = Field(None, description="Percentage composition of the vein")


class SMetasomatite(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    metasomatite_type: str = Field(..., description="Type of metasomatite")
    percentage: Optional[float] = Field(None, description="Percentage composition of the metasomatite")



class SRareOreMineralization(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    rare_ore_mineral: str = Field(..., description="Name of the rare ore mineral")


class SAccessoryMineral(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    sample_id: int = Field(..., description="ID of the associated sample")
    accessory_mineral: str = Field(..., description="Name of the accessory mineral")