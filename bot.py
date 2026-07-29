import os
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

SITE_URL = "https://mudarris-akadmeiyasi.netlify.app/"


def load_token():
    token = os.environ.get("BOT_TOKEN")
    if token:
        return token.strip()
    token_path = os.path.join(os.path.dirname(__file__), "token.txt")
    with open(token_path, "r", encoding="utf-8") as f:
        return f.readline().strip()


BOT_TOKEN = load_token()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("📚 Ilovani ochish", web_app=WebAppInfo(url=SITE_URL))
    ]])
    text = (
        f"Assalomu alaykum, {user.first_name}! 👋\n\n"
        "*Mudarris Akademiyasi*ga xush kelibsiz — arab tili grammatikasini "
        "qiziqarli mashqlar orqali o'rganing.\n\n"
        "Boshlash uchun quyidagi tugmani bosing:"
    )
    await update.message.reply_text(text, reply_markup=keyboard, parse_mode="Markdown")


def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    logger.info("Bot ishga tushdi...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
