import os from pymongo import MongoClient from dotenv import load_dotenv from datetime import datetime

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI") client = MongoClient(MONGO_URI) db = client["price_tracker_bot"] users_col = db["users"] products_col = db["products"]

def add_user(user_id): if not users_col.find_one({"user_id": user_id}): users_col.insert_one({"user_id": user_id, "created_at": datetime.utcnow()})

def add_product(user_id, title, price, url, affiliate_url, platform): product = { "user_id": user_id, "title": title, "price": price, "url": url, "affiliate_url": affiliate_url, "platform": platform, "created_at": datetime.utcnow() } products_col.insert_one(product)

def get_user_products(user_id): return list(products_col.find({"user_id": user_id}))

