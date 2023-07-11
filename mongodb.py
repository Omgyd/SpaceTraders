import os
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

client = MongoClient(os.environ.get("MONGODB_URI"))

db = client['Space_traders']

tokens = db.token


def insert_token(token):
    token_id = token
    new_token = {
        'token': token_id
        }
    tokens.insert_one(new_token)


def get_most_recent_token():
    collection = tokens.find({}).sort([("_id", pymongo.DESCENDING)]).limit(1)
    for item in collection:
        return item['token']
    

