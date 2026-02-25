import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("TOKEN")
GROUP_ID = -1003875236057

if not TOKEN:
    raise RuntimeError("TOKEN topilmadi")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Murojaatingizni yozing:")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    message = (
        f"📩 Yangi murojaat\n\n"
        f"👤 Ism: {user.first_name}\n"
        f"🆔 ID: {user.id}\n\n"
        f"📝 Matn:\n{text}"
    )

    await context.bot.send_message(chat_id=GROUP_ID, text=message)
    await update.message.reply_text("Yuborildi ✅")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

app.run_polling()