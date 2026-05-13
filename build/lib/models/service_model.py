
from bson import ObjectId, json_util

from src.db.db import startConnection


class ServiceModel:
    def __init__(self, _id: ObjectId, service_type:str, address: str="", description: str="",) -> None:
        self._id: ObjectId = _id
        self.service_type:str = service_type
        self.address:str = address
        self.description: str = description
        self.last_updated: int = 0

    @classmethod
    def from_dict(cls, d):
        return cls(
            _id=d.get("_id") or None,
            service_type=d.get("service_type"),
            address=d.get("address"),
            description=d.get("description"),

        )
    def to_create_dict(self) -> dict:
        return {
            "service_type": self.service_type,
            "address": self.address,
            "description": self.description,
            "last_updated": self.last_updated
        }

    @classmethod
    def get_services(cls) -> list[dict]:
        db = startConnection()
        return db['services'].find().to_list()
    
    @classmethod
    def get_service_by_type(cls, service_type: str) -> dict:
        db = startConnection()
        return db['services'].find({"service_type": service_type}).sort("last_updated", -1).limit(1).to_list()

    def create_service(self)-> dict:
        db = startConnection()
        res = db['services'].insert_one(self.to_create_dict())
        return db['services'].find_one(res.inserted_id)

    def update_service(self) -> dict:
        db = startConnection()
        res = db['services'].update_one({"_id": self._id}, {"$set":self.to_create_dict()})
        return db['services'].find_one(res.upserted_id)

    @classmethod
    def delete_service(cls, service_id: str) -> bool:
        db = startConnection()
        res = db['services'].delete_one({"_id": ObjectId(service_id)})
        return  res.deleted_count >= 1
