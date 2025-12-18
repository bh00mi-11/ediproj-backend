from django.conf import settings
from pymongo import MongoClient
import gridfs

def get_db():
    client = MongoClient(settings.MONGO_URI)
    db = client[settings.MONGO_DB_NAME]
    return db

def get_gridfs():
    db = get_db()
    fs = gridfs.GridFS(db)
    return fs
