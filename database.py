from pymongo import MongoClient
import os

MONGO_URL = os.getenv("MONGO_URL")
client = MongoClient(MONGO_URL)
db = client["price_tracker"]

def add_user(user_id):
    if not db.users.find_one({"user_id": user_id}):
        db.users.insert_one({"user_id": user_id})

def add_product(user_id, url, details):
    db.products.insert_one({
        "user_id": user_id,
        "url": url,
        "title": details["title"],
        "price": details["price"],
        "image": details["image"],
    })

def get_user_products(user_id):
    return list(db.products.find({"user_id": user_id}))