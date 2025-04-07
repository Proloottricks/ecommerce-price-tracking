import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
from tracker import get_price_details
from affiliate import convert_to_affiliate
from database import add_user, add_product, get_user_products

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)
    await update.message.reply_text(
        f"Hi {user.first_name}! Send me any product link from Amazon, Flipkart, Ajio or Shopsy."
    )

# Handle incoming product links
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    url = update.message.text.strip()

    if any(x in url for x in ["amazon", "flipkart", "ajio", "shopsy"]):
        msg = await update.message.reply_text("Fetching product details...")
        product = get_price_details(url)

        if product:
            affiliate_url = convert_to_affiliate(url)
            add_product(user.id, product, affiliate_url)
            reply_text = f"**{product['title']}**\n\nPrice: ₹{product['price']}\n\n[Buy Now]({affiliate_url})"
            await msg.edit_text(reply_text, parse_mode="Markdown", disable_web_page_preview=False)
        else:
            await msg.edit_text("Failed to fetch product details.")
    else:
        await update.message.reply_text("Please send a valid product URL from supported sites.")

# /myproducts command
async def my_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    products = get_user_products(user_id)

    if not products:
        await update.message.reply_text("You have not added any products yet.")
        return

    buttons = [
        [InlineKeyboardButton(p["title"]