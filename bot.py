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

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id, user.username)
    await update.message.reply_text(
        "Welcome to the Price Tracker Bot!\n\n"
        "Send me an Amazon, Flipkart, Ajio, or Shopsy product link to start tracking.\n\n"
        "Use /myproducts to view your tracked items."
    )


async def track_product(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    url = update.message.text.strip()

    await update.message.reply_text("Fetching product details...")

    try:
        product = get_price_details(url)
        if not product:
            await update.message.reply_text("Failed to fetch product details.")
            return

        product["url"] = convert_to_affiliate(url)
        add_product(user_id, product)

        await update.message.reply_photo(
            photo=product["image"],
            caption=f"*{product['title']}*\nPrice: ₹{product['price']}\n{product['url']}",
            parse_mode="Markdown",
        )
    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text("Something went wrong while processing the link.")


async def my_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    products = get_user_products(user_id)

    if not products:
        await update.message.reply_text("You have not tracked any products yet.")
        return

    keyboard = [
        [InlineKeyboardButton(p["title"], url=p["url"])]
        for p in products
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Your Tracked Products:", reply_markup=reply_markup)


def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("myproducts", my_products))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_product))

    app.run_polling()


if __name__ == "__main__":
    main()