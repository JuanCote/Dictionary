import os

from pymongo import MongoClient


MONGODB_URI = os.getenv('MONGODB_URI')
client = MongoClient(MONGODB_URI)
db = client.DictionaryTelegramBot

dictionary = db.dictionary
