from telegram.ext import Updater, CommandHandler
from scraper import get_price_data
from database import insert_product, get_all_products
from utils import get_domain_name
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")

def start(update, context):
    update.message.reply_text("Send a product link from Amazon, Flipkart, Ajio, or Shopsy to track its price.")

def track_price(update, context):
    url = update.message.text.strip()
    chat_id = update.message.chat_id

    domain = get_domain_name(url)
    if domain not in ["amazon", "flipkart", "ajio", "shopsy"]:
        update.message.reply_text("Only Amazon, Flipkart, Ajio, and Shopsy links are supported.")
        return

    data = get_price_data(url)
    if data is None:
        update.message.reply_text("Failed to fetch product data. Check the link.")
        return

    insert_product(chat_id, url, data['title'], data['price'], data['image'])

    update.message.reply_text(
        f"Tracking started for:\n\n{data['title']}\n\nPrice: ₹{data['price']}\n\nYou’ll be notified on price drops!"
    )

def list_products(update, context):
    chat_id = update.message.chat_id
    products = get_all_products(chat_id)

    if not products:
        update.message.reply_text("No products tracked yet.")
        return

    msg = "Your Tracked Products:\n\n"
    for p in products:
        msg += f"{p['title']} - ₹{p['price']}\n{p['url']}\n\n"
    update.message.reply_text(msg)

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("list", list_products))
    dp.add_handler(CommandHandler("track", track_price))