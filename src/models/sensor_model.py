
from src.db.db import startConnection
from bson import json_util, ObjectId


class SensorModel:
    def __init__(self, _id: ObjectId, name: str="", model: str="", unit: str="") -> None:
        self._id: ObjectId
        self.name: str = name
        self.model: str = model
        self.unit: str = unit

    @classmethod
    def from_dict(cls, d):
        return cls(
            _id=d.get("_id") or None,
            name=d.get("name"),
            model=d.get("model"),
            unit=d.get("unit"),
        )
    def toCreateDict(self) -> dict:
        return {
            "name": self.name,
            "model": self.model,
            "unit": self.unit
        }
    
    @classmethod
    def getSensors(cls) -> list[dict]:
        db = startConnection()
        ls =  db['sensors'].find().to_list()
        print(ls)
        return ls
    
    def createSensor(self)-> dict:
        db = startConnection()
        res = db['sensors'].insert_one(self.toCreateDict())
        return json_util.dumps(db['sensors'].find_one(res.inserted_id))
   
    def updateSensor(self) -> dict:
        db = startConnection()
        res = db['sensors'].update_one({"_id": self._id}, {"$set":self.__dict__})        
        return json_util.dumps(db['sensors'].find_one(res.upserted_id))
    
    @classmethod
    def deleteSensor(_cls, id: str) -> bool:
        db = startConnection()
        res = db['sensors'].delete_one({"_id": ObjectId(id)})
        return  res.deleted_count >= 1;

   