# main.py

import os
import re
import logging
import pymongo
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import scrape_amazon, scrape_flipkart, scrape_ajio, scrape_shopsy

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# Environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# MongoDB setup
client = pymongo.MongoClient(MONGO_URI)
db = client["price_tracker"]
collection = db["tracked_items"]

# Get site name from URL
def get_site_name(url: str) -> str:
    if "amazon" in url:
        return "amazon"
    elif "flipkart" in url:
        return "flipkart"
    elif "ajio" in url:
        return "ajio"
    elif "shopsy" in url:
        return "shopsy"
    else:
        return "unknown"

# Scrape dispatcher
def scrape_price(url: str):
    site = get_site_name(url)
    if site == "amazon":
        return scrape_amazon(url)
    elif site == "flipkart":
        return scrape_flipkart(url)
    elif site == "ajio":
        return scrape_ajio(url)
    elif site == "shopsy":
        return scrape_shopsy(url)
    else:
        return {"error": "Unsupported site"}

# Start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Price Tracker Bot!\nSend me a product link from Amazon, Flipkart, Ajio, or Shopsy.")

# Handle product link
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()

    if not re.match(r'^https?://', url):
        await update.message.reply_text("Please send a valid product URL starting with http/https.")
        return

    site = get_site_name(url)
    if site == "unknown":
        await update.message.reply_text("Only Amazon, Flipkart, Ajio, and Shopsy links are supported.")
        return

    result = scrape_price(url)

    if "error" in result:
        await update.message.reply_text(f"Error scraping product: {result['error']}")
        return

    # Save to database
    collection.insert_one({
        "user_id": update.message.from_user.id,
        "url": url,
        "site": site,
        "title": result["title"],
        "price": result["price"]
    })

    await update.message.reply_text(f"Tracking started!\n\nTitle: {result['title']}\nPrice: {result['price']}")

# Main function
if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("track", handle_message))
    app.add_handler(CommandHandler("add", handle_message))
    app.add_handler(CommandHandler("price", handle_message))
    app.add_handler(CommandHandler("check", handle_message))
    app.add_handler(CommandHandler("watch", handle_message))
    app.add_handler(CommandHandler("monitor", handle_message))
    app.add_handler(CommandHandler("link", handle_message))
    app.add_handler(CommandHandler("url", handle_message))
    app.add_handler(CommandHandler("product", handle_message))
    app.add_handler(CommandHandler("start_tracking", handle_message))

    # Handle any plain message as URL
    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()