import os
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters
from dotenv import load_dotenv
from tracker import get_price_details
from affiliate import convert_to_affiliate
from database import add_user, add_product, get_user_products

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URL = os.getenv("MONGO_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    await update.message.reply_text(
        f"Hello {user.first_name}! Send me an Amazon, Flipkart, Ajio, or Shopsy product link to track its price."
    )
    add_user(user.id)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text.strip()

    if any(site in text for site in ["amazon", "flipkart", "ajio", "shopsy"]):
        await update.message.reply_text("Getting product details...")

        details = get_price_details(text)
        if not details:
            await update.message.reply_text("Couldn't fetch product details. Please try a valid URL.")
            return

        affiliate_link = convert_to_affiliate(text)
        add_product(user.id, affiliate_link, details)

        await update.message.reply_photo(
            photo=details["image"],
            caption=f"**{details['title']}**\n\nCurrent Price: ₹{details['price']}\n\n[Buy Now]({affiliate_link})",
            parse_mode="Markdown",
        )
    else:
        await update.message.reply_text("Please send a valid product link.")


async def track(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    products = get_user_products(user.id)

    if not products:
        await update.message.reply_text("You're not tracking any products yet.")
        return

    keyboard = [
        [InlineKeyboardButton(p["title"][:50], url=p["url"])] for p in products
    ]

    await update.message.reply_text(
        "Here are your tracked products:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("track", track))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot is running...")
    app.run_polling()