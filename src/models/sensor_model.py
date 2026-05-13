from bson import ObjectId

from src.db.db import startConnection


class SensorModel:
    def __init__(
        self, _id: ObjectId, tp: str = "", model: str = "", unit: str = ""
    ) -> None:
        self._id: ObjectId = _id
        self.type: str = tp
        self.model: str = model
        self.unit: str = unit

    @classmethod
    def from_dict(cls, d):
        return cls(
            _id=d.get("_id") or None,
            tp=d.get("type"),
            model=d.get("model"),
            unit=d.get("unit"),
        )

    def to_create_dict(self) -> dict:
        return {"type": self.type, "model": self.model, "unit": self.unit}

    def to_dict(self) -> dict:
        return {
            "_id": self._id,
            "type": self.type,
            "model": self.model,
            "unit": self.unit,
        }

    @classmethod
    def get_sensors(cls) -> list[dict]:
        db = startConnection()
        return db["sensors"].find().to_list()

    def create_sensor(self) -> dict:
        db = startConnection()
        res = db["sensors"].insert_one(self.to_create_dict())
        return db["sensors"].find_one(res.inserted_id)

    def update_sensor(self) -> dict:
        db = startConnection()
        res = db["sensors"].update_one(
            {"_id": self._id}, {"$set": self.to_create_dict()}, upsert=False
        )
        return db["sensors"].find_one(res.upserted_id)

    @classmethod
    def delete_sensor(cls, sensor_id: str) -> bool:
        db = startConnection()
        res = db["sensors"].delete_one({"_id": ObjectId(sensor_id)})
        return res.deleted_count >= 1
