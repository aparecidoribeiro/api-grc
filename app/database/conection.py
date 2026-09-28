import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_url = os.getenv("mongo_url")

client = MongoClient(mongo_url)

db = client.get_default_database()