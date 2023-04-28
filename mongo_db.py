import os

from pymongo import MongoClient


MONGODB_URI = os.getenv('mongodb-uri')
client = MongoClient(MONGODB_URI)
db = client.DictionaryTelegramBot

dictionary = db.dictionary
