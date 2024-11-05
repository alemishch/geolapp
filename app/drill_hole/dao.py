from app.dao.base import BaseDAO
from app.samples.models import DrillHole


class DrillHoleDAO(BaseDAO):
    model = DrillHole
    default_relationships = [
        DrillHole.samples
    ]