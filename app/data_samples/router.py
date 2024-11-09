from fastapi import APIRouter, Depends, Form, File, UploadFile
from fastapi.responses import JSONResponse
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
    SAccessoryMineral,
    SPhotosAdd,
    SMineralCompositionAdd,
    SOreMineralizationAdd,
    SVeinAdd,
    SMetasomatiteAdd,
    SRareOreMineralizationAdd,
    SAccessoryMineralAdd
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
        "create_schema": SPhotosAdd,
        "rb_schema": RBPhotos
    },
    "mineral_composition": {
        "dao": MineralCompositionDAO,
        "schema": SMineralComposition,
        "create_schema": SMineralCompositionAdd,
        "rb_schema": RBMineralComposition
    },
    "ore_mineralization": {
        "dao": OreMineralizationDAO,
        "schema": SOreMineralization,
        "create_schema": SOreMineralizationAdd,
        "rb_schema": RBOreMineralization
    },
    "vein": {
        "dao": VeinDAO,
        "schema": SVein,
        "create_schema": SVeinAdd,
        "rb_schema": RBVein
    },
    "metasomatite": {
        "dao": MetasomatiteDAO,
        "schema": SMetasomatite,
        "create_schema": SMetasomatiteAdd,
        "rb_schema": RBMetasomatite
    },
    "rare_ore_mineralization": {
        "dao": RareOreMineralizationDAO,
        "schema": SRareOreMineralization,
        "create_schema": SRareOreMineralizationAdd,
        "rb_schema": RBRareOreMineralization
    },
    "accessory_mineral": {
        "dao": AccessoryMineralDAO,
        "schema": SAccessoryMineral,
        "create_schema": SAccessoryMineralAdd,
        "rb_schema": RBAccessoryMineral
    }
}

    
for model_name, components in MODEL_MAPPINGS.items():
    dao = components["dao"]
    create_schema = components["create_schema"]
    schema = components["schema"]
    rb_schema = components["rb_schema"]
    
    if model_name == "photos":
        @router.post(f"/{model_name}/add/", response_model=rb_schema, summary=f"Добавить {model_name}")
        async def add_photos(
            sample_id: int = Form(...),
            photo_type: str = Form(...),
            file: UploadFile = File(...),
            dao=Depends(lambda: dao)
        ):
            ALLOWED_TYPES = ["macro", "straight_light", "reflected_light"]
            if photo_type not in ALLOWED_TYPES:
                raise HTTPException(status_code=400, detail="Неверный тип фотографии.")
            
            folder_path = os.path.join("img", photo_type, f"sample_{sample_id}")
            os.makedirs(folder_path, exist_ok=True)
            file_location = os.path.join(folder_path, file.filename)
            
            try:
                with open(file_location, "wb") as buffer:
                    shutil.copyfileobj(file.file, buffer)
                
                # Save to DB
                photo_record = await dao.add(sample_id=sample_id, photo_type=photo_type, file_path=file_location)
                return photo_record
            except Exception:
                raise HTTPException(status_code=500, detail="Ошибка при загрузке фотографии.")
            
        pass  
    else:
        @router.post(f"/{model_name}/add/", response_model=rb_schema, summary=f"Добавить {model_name}")
        async def add_model_data(data: create_schema, dao=Depends(lambda: dao)):
            try:
                new_record = await dao.add(**data.dict())
                if new_record:
                    return new_record
                else:
                    raise HTTPException(status_code=400, detail=f"Ошибка при добавлении {model_name}.")
            except HTTPException as he:
                raise he
            except Exception:
                raise HTTPException(status_code=500, detail="Внутренняя ошибка сервера.")
    
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
            return JSONResponse(
                status_code=200,
                content={"message": "Нет данных для отображения", "error": True}
            )
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
