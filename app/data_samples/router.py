from fastapi import APIRouter, Depends, HTTPException
from typing import List, Union

from app.data_samples.dao import (
    PhotosDAO,
    MineralCompositionDAO,
    OreMineralizationDAO,
    VeinDAO,
    MetasomatiteDAO,
    RareOreMineralizationDAO,
    AccessoryMineralDAO
)

from app.data_samples.schemas import (
    SPhotos,
    SMineralComposition,
    SOreMineralization,
    SVein,
    SMetasomatite,
    SRareOreMineralization,
    SAccessoryMineral
)

from app.data_samples.rb import (
    RBPhotos,
    RBMineralComposition,
    RBOreMineralization,
    RBVein,
    RBMetasomatite,
    RBRareOreMineralization,
    RBAccessoryMineral
)

router = APIRouter(
    prefix="/additional_models",
    tags=["Additional Models"]
)

MODEL_MAPPINGS = {
    "photos": {
        "dao": PhotosDAO,
        "schema": SPhotos,
        "rb_schema": RBPhotos
    },
    "mineral_composition": {
        "dao": MineralCompositionDAO,
        "schema": SMineralComposition,
        "rb_schema": RBMineralComposition
    },
    "ore_mineralization": {
        "dao": OreMineralizationDAO,
        "schema": SOreMineralization,
        "rb_schema": RBOreMineralization
    },
    "vein": {
        "dao": VeinDAO,
        "schema": SVein,
        "rb_schema": RBVein
    },
    "metasomatite": {
        "dao": MetasomatiteDAO,
        "schema": SMetasomatite,
        "rb_schema": RBMetasomatite
    },
    "rare_ore_mineralization": {
        "dao": RareOreMineralizationDAO,
        "schema": SRareOreMineralization,
        "rb_schema": RBRareOreMineralization
    },
    "accessory_mineral": {
        "dao": AccessoryMineralDAO,
        "schema": SAccessoryMineral,
        "rb_schema": RBAccessoryMineral
    }
}

for model_name, components in MODEL_MAPPINGS.items():
    dao = components["dao"]
    schema = components["schema"]
    rb_schema = components["rb_schema"]
    
    async def get_all(model_name=model_name, dao=dao, schema=schema, rb_schema=rb_schema, request_body: rb_schema = Depends()):
        """
        Retrieve all records for the given model with optional filters.
        """
        filters = request_body.to_dict()
        records = await dao.find_all(**filters)
        return records
    
    async def get_by_filter(model_name=model_name, dao=dao, schema=schema, rb_schema=rb_schema, request_body: rb_schema = Depends()):
        """
        Retrieve records based on filter criteria.
        """
        filters = request_body.to_dict()
        records = await dao.find_all(**filters)
        if not records:
            return {'message': f'No records found for {model_name} with specified filters.'}
        return records

    async def find_by_sample_id(sample_id: int, model_name=model_name, dao=dao, schema=schema):
        """
        Retrieve all {model_name} records associated with a specific sample_id.
        """
        records = await dao.find_all(sample_id=sample_id)
        if not records:
            return {'message': f'No {model_name} records found for sample_id {sample_id}.'}
        return records
    
    async def get_by_id(id: int, dao=dao, schema=schema):
        record = await dao.find_one_or_none_by_id(id)
        if record is None:
            raise HTTPException(status_code=404, detail=f"{model_name.capitalize()} not found")
        return record
    
    # Register the endpoints with appropriate paths and metadata
    router.get(f"/{model_name}/", summary=f"Get all {model_name} records", response_model=List[schema])(get_all)
    router.get(f"/{model_name}/by_filter", summary=f"Get {model_name} records by filter", response_model=Union[List[schema], dict])(get_by_filter)
    router.get(f"/{model_name}/{{id}}", summary=f"Get {model_name} by ID", response_model=schema)(get_by_id)
    router.get(f"/{model_name}/sample/{{sample_id}}",summary=f"Get {model_name} by sample_id",response_model=List[schema])(find_by_sample_id)
