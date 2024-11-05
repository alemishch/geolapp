from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class RBPhotos(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the photo")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    macro: Optional[str] = Field(None, description="URL or path to macro photo")
    straight_light: Optional[str] = Field(None, description="URL or path to straight light photo")
    reflected_light: Optional[str] = Field(None, description="URL or path to reflected light photo")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class RBMineralComposition(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the mineral composition")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    mineral_name: Optional[str] = Field(None, description="Name of the mineral")
    percentage: Optional[float] = Field(None, description="Percentage composition of the mineral")
    main_secondary: Optional[str] = Field(None, description="Indicates if the mineral is main or secondary")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class RBOreMineralization(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the ore mineralization")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    mineral_name: Optional[str] = Field(None, description="Name of the ore mineral")
    percentage: Optional[float] = Field(None, description="Percentage composition of the ore mineral")
    main_secondary: Optional[str] = Field(None, description="Indicates if the ore mineral is main or secondary")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class RBVein(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the vein")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    vein_name: Optional[str] = Field(None, description="Name of the vein")
    percentage: Optional[float] = Field(None, description="Percentage composition of the vein")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class RBMetasomatite(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the metasomatite")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    metasomatite_type: Optional[str] = Field(None, description="Type of metasomatite")
    percentage: Optional[float] = Field(None, description="Percentage composition of the metasomatite")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class RBRareOreMineralization(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the rare ore mineralization")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    rare_ore_mineral: Optional[str] = Field(None, description="Name of the rare ore mineral")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data


class RBAccessoryMineral(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
    
    id: Optional[int] = Field(None, description="Unique identifier of the accessory mineral")
    sample_id: Optional[int] = Field(None, description="ID of the associated sample")
    accessory_mineral: Optional[str] = Field(None, description="Name of the accessory mineral")
    
    def to_dict(self) -> dict:
        data = self.dict(exclude_unset=True)
        filtered_data = {key: value for key, value in data.items() if value is not None}
        return filtered_data