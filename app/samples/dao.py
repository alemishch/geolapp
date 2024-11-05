from app.dao.base import BaseDAO
from app.samples.models import Sample


class SampleDAO(BaseDAO):
    model = Sample
    default_relationships = [
        Sample.drill_hole_rel,
        Sample.photos,
        Sample.mineral_compositions,
        Sample.ore_mineralizations,
        Sample.veins,
        Sample.metasomatites,
        Sample.rare_ore_minerals,
        Sample.accessory_minerals
    ]