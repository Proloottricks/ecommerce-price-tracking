from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
collection = db["products"]

def insert_product(chat_id, url, title, price, image):
    collection.update_one(
        {"chat_id": chat_id, "url": url},
        {"$set": {"title": title, "price": price, "image": image}},
        upsert=True
    )

def get_all_products(chat_id):
    return list(collection.find({"chat_id": chat_id}, {"_id": 0}))