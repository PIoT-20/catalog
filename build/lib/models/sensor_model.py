from json.encoder import JSONEncoder

from src.db.db import startConnection


class SensorModel:
    def __init__(self, id: str, name: str, model: str, unit: str) -> None:
        self.id: str = id
        self.name: str = name
        self.model: str = model
        self.unit: str = unit

    def createSensor(self):
        db = startConnection()
        db['sensors'].insert_one(JSONEncoder().encode(self))
