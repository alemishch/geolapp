from app.dao.base import BaseDAO
from app.samples.models import (
    Photos,
    MineralComposition,
    OreMineralization,
    Vein,
    Metasomatite,
    RareOreMineralization,
    AccessoryMineral
)


class PhotosDAO(BaseDAO):
    model = Photos
    default_relationships = [
        Photos.sample
    ]


class MineralCompositionDAO(BaseDAO):
    model = MineralComposition
    default_relationships = [
        MineralComposition.sample
    ]


class OreMineralizationDAO(BaseDAO):
    model = OreMineralization
    default_relationships = [
        OreMineralization.sample
    ]


class VeinDAO(BaseDAO):
    model = Vein
    default_relationships = [
        Vein.sample
    ]


class MetasomatiteDAO(BaseDAO):
    model = Metasomatite
    default_relationships = [
        Metasomatite.sample
    ]


class RareOreMineralizationDAO(BaseDAO):
    model = RareOreMineralization
    default_relationships = [
        RareOreMineralization.sample
    ]


class AccessoryMineralDAO(BaseDAO):
    model = AccessoryMineral
    default_relationships = [
        AccessoryMineral.sample
    ]
