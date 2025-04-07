import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from scraper import scrape_and_store_price
from database import get_product, init_db
from utils import format_price_message

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the Price Tracker Bot! Send a product link to start tracking.")

async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.message.chat_id
    result = await scrape_and_store_price(url, chat_id)
    await update.message.reply_text(result)

async def check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    chat_id = update.message.chat_id
    product = get_product(url, chat_id)
    if product:
        msg = format_price_message(product)
    else:
        msg = "No product found for this link."
    await update.message.reply_text(msg)

if __name__ == "__main__":
    init_db()
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))
    app.add_handler(CommandHandler("check", check))

    app.run_polling()