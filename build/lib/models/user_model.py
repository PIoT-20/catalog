from src.db.db import startConnection
from bson import ObjectId


class UserModel:
    def __init__(self, _id: ObjectId, name: str = "", email: str = "", password: str = "") -> None:
        self._id: ObjectId = _id
        self.name: str = name
        self.email: str = email
        self.password: str = password

    @classmethod
    def from_dict(cls, d):
        return cls(
            _id=d.get("_id") or None,
            name=d.get("name"),
            email=d.get("email"),
            password=d.get("password"),
        )

    def to_create_dict(self) -> dict:
        return {
            "name": self.name,
            "email": self.email,
            "password": self.password
        }

    @classmethod
    def get_users(cls) -> list[dict]:
        db = startConnection()
        return db['users'].find().to_list()

    def create_user(self) -> dict:
        db = startConnection()
        res = db['users'].insert_one(self.to_create_dict())
        return db['users'].find_one(res.inserted_id)

    def update_user(self) -> dict:
        db = startConnection()
        res = db['users'].update_one({"_id": self._id}, {"$set": self.to_create_dict()}, upsert=False)
        return db['users'].find_one(res.upserted_id)

    @classmethod
    def delete_user(cls, user_id: str) -> bool:
        db = startConnection()
        res = db['users'].delete_one({"_id": ObjectId(user_id)})
        return res.deleted_count >= 1

