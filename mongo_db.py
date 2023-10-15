import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
print(MONGODB_URI)
client = MongoClient(MONGODB_URI)
db = client.dictionary_bot

users = db.users
