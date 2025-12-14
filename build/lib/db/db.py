import os

from pymongo.database import Database
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


def startConnection() -> Database:
    uri: (str | None) = os.getenv("MONGO_DB")
    if uri is None:
        raise ValueError("MONGO_DB environment variable is not set")
    client: MongoClient = MongoClient(uri, server_api=ServerApi('1'))
    return client["catalog"]
