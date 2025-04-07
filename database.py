import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
collection = db["products"]

def init_db():
    client.admin.command('ping')  # Check connection

def save_product(data):
    collection.update_one(
        {"chat_id": data["chat_id"], "url": data["url"]},
        {"$set": data},
        upsert=True
    )

def get_product(url, chat_id):
    return collection.find_one({"chat_id": chat_id, "url": url})