from bson import ObjectId, json_util
from src.db.db import startConnection
from src.models.sensor_model import SensorModel
from src.models.connection_info_model import ConnectionInfo


class DeviceModel:
    def __init__(self, _id: ObjectId,_user_id: ObjectId, device_type:str, location: str,connection_info: ConnectionInfo, description: str="", sensors: list[SensorModel]=[]) -> None:
        self._id: ObjectId = _id
        self.device_type: str = device_type
        self.location: str = location
        self.connection_info: ConnectionInfo = connection_info
        self.description: str = description
        self.sensors: list[SensorModel]=  sensors
        self.user_id: ObjectId = _user_id

    @classmethod
    def from_dict(cls, d):
        return cls(
            type=d.get("type"),
            model=d.get("model"),
            unit=d.get("unit")
        )
    
    def to_dict(self) -> dict:
        return {
            "type": self.type,
            "model": self.model,
            "unit": self.unit
        }

class ConnectionInfoModel:
    def __init__(self, data: dict) -> None:
        if not isinstance(data, dict):
            raise ValueError("Connection info data must be a dictionary")
        if "protocol" not in data or not data["protocol"]:
            raise ValueError("Connection info must contain a 'protocol' field")
        self.data = data

    @classmethod
    def from_dict(cls, d):
        if not d:
            raise ValueError("Connection info cannot be None or empty")
        return cls(d)
    
    def to_dict(self) -> dict:
        return self.data

class DeviceModel:
    def __init__(self, _id: ObjectId,_user_id: ObjectId, device_type:str, location: str, connection_info: ConnectionInfoModel, sensors: list[SensorModel], description: str="") -> None:
        self._id: ObjectId = _id
        self.device_type: str = device_type
        self.location: str = location
        self.connection_info: ConnectionInfoModel = connection_info
        self.sensors: list[SensorModel] =  sensors
        self.user_id: ObjectId = _user_id
        self.description: str = description

    @classmethod
    def from_dict(cls, d):
        sensors = [SensorModel.from_dict(s) for s in d.get("sensors", [])]
        connection_info = ConnectionInfoModel.from_dict(d.get("connection_info"))
            
        return cls(
            _id=d.get("_id") or None,
            device_type=d.get("device_type"),
            location=d.get("location"),
            connection_info=d.get("connection_info"),
            description=d.get("description"),
            location=d.get("location"),
            sensors=sensors,
            user_id=d.get("user_id"),
            connection_info=connection_info
        )
    def to_create_dict(self) -> dict:
        return {
            "device_type": self.device_type,
            "description": self.description,
            "location": self.location,
            "sensors": [s.to_dict() for s in self.sensors],
            "user_id": self.user_id,
            "connection_info": self.connection_info.to_dict()
        }

    @classmethod
    def get_devices(cls) -> list[dict]:
        db = startConnection()
        return db['devices'].find().to_list()

    @classmethod
    def get_devices_by_client_and_device_id(cls, client_id: ObjectId, device_id: ObjectId) -> list[dict]:
        db = startConnection()
        return db['devices'].find({"user_id": client_id, "_id":device_id}).to_list()

    @classmethod
    def get_devices_by_client_id(cls, client_id: ObjectId) -> list[dict]:
        db = startConnection()
        return db['devices'].find({"user_id": client_id}).to_list()

    def create_device(self)-> dict:
        db = startConnection()
        res = db['devices'].insert_one(self.to_create_dict())
        return db['devices'].find_one(res.inserted_id)

    def update_device(self) -> dict:
        db = startConnection()
        res = db['devices'].update_one({"_id": self._id}, {"$set":self.to_create_dict()}, upsert=False)
        return db['devices'].find_one(res.upserted_id)

    @classmethod
    def delete_device(cls, device_id: str) -> bool:
        db = startConnection()
        res = db['devices'].delete_one({"_id": ObjectId(device_id)})
        return  res.deleted_count >= 1
