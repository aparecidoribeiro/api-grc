import os
from dotenv import load_dotenv
from pymongo import AsyncMongoClient

load_dotenv()

mongo_url = os.getenv("mongo_url")

client = AsyncMongoClient(mongo_url)

db = client["bancogrc"]

#Collection
users_collection = db["users"]
families_collection = db["family"]