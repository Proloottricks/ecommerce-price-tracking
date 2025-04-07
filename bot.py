import os import logging from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters from dotenv import load_dotenv from tracker import get_price_details from affiliate import convert_to_affiliate from database import add_user, add_product, get_user_products

load_dotenv() logging.basicConfig(level=logging.INFO)

BOT_TOKEN = os.getenv("BOT_TOKEN")

Start command

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id add_user(user_id) await update.message.reply_text("Welcome to the Price Tracker Bot!\nSend me a product link from Amazon, Flipkart, Ajio, or Shopsy.")

Handle product URL

async def handle_url(update: Update, context: ContextTypes.DEFAULT_TYPE): url = update.message.text user_id = update.effective_user.id

price_info = get_price_details(url)
if not price_info:
    await update.message.reply_text("Invalid or unsupported link. Please use Amazon, Flipkart, Ajio, or Shopsy.")
    return

title, price, platform = price_info
affiliate_url = convert_to_affiliate(url, platform)

add_product(user_id, title, price, url, affiliate_url, platform)

buttons = [
    [InlineKeyboardButton("Buy Now", url=affiliate_url)],
    [InlineKeyboardButton("Track Price", callback_data=f"track|{url}")]
]

await update.message.reply_text(
    f"*{title}*\nPlatform: {platform}\nCurrent Price: ₹{price}",
    parse_mode='Markdown',
    reply_markup=InlineKeyboardMarkup(buttons)
)

Handle button press

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE): query = update.callback_query await query.answer() data = query.data if data.startswith("track"): await query.edit_message_text("Product added to your tracking list!")

Show tracked products

async def mylist(update: Update, context: ContextTypes.DEFAULT_TYPE): user_id = update.effective_user.id products = get_user_products(user_id)

if not products:
    await update.message.reply_text("You are not tracking any products yet.")
    return

message = "Your Tracked Products:\n\n"
for p in products:
    message += f"{p['title']} (from {p['platform']}) - ₹{p['price']}\n{p['affiliate_url']}\n\n"

await update.message.reply_text(message)

app = ApplicationBuilder().token(BOT_TOKEN).build() app.add_handler(CommandHandler("start", start)) app.add_handler(CommandHandler("mylist", mylist)) app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_url)) app.add_handler(CallbackQueryHandler(button_handler))

if name == 'main': app.run_polling()


