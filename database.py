import os
from pymongo import MongoClient
from datetime import datetime

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["price_tracker"]
collection = db["products"]

def store_price(url, title, price, site):
    data = {
        "url": url,
        "title": title,
        "price": price,
        "site": site,
        "timestamp": datetime.utcnow()
    }
    collection.insert_one(data)