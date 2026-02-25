import os
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("TOKEN")
GROUP_ID = -1003875236057

if not TOKEN:
    raise RuntimeError("TOKEN env topilmadi. Railway Variables ga TOKEN qo‘shing.")

# Guruhdagi message_id → user_id map
user_messages = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Murojaatingizni yozing:")

# User yozganda
async def handle_user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text

    message = (
        f"📩 Yangi murojaat\n\n"
        f"👤 Ism: {user.first_name}\n"
        f"🆔 ID: {user.id}\n\n"
        f"📝 Matn:\n{text}"
    )

    sent_message = await context.bot.send_message(
        chat_id=GROUP_ID,
        text=message
    )

    # Guruhdagi message_id ni user bilan bog‘laymiz
    user_messages[sent_message.message_id] = user.id


    # 2-xabar (alohida xabar)
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Assalomu aleykum! Murojaatingiz qabul qilindi ✅\nSizga tez orada javob yo‘llayman."
    )

# Admin guruhda reply qilganda
async def handle_group_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Faqat o‘sha guruhdan kelgan reply bo‘lsin
    if update.effective_chat and update.effective_chat.id != GROUP_ID:
        return

    if not update.message or not update.message.reply_to_message:
        return

    replied_msg_id = update.message.reply_to_message.message_id

    if replied_msg_id not in user_messages:
        return

    user_id = user_messages[replied_msg_id]
    reply_text = update.message.text or ""

    if not reply_text.strip():
        return

    await context.bot.send_message(
        chat_id=user_id,
        text=f"\n\n{reply_text}"
    )

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND, handle_user_message))
app.add_handler(MessageHandler(filters.ChatType.GROUPS & filters.TEXT, handle_group_reply))

app.run_polling()