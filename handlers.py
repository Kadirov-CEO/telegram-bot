import logging
import os

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from keyboards import main_menu_keyboard

logger = logging.getLogger(__name__)

LOGO_PATH = os.path.join(os.path.dirname(__file__), "image.png")


async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    if user is None or update.message is None:
        return

    logger.info("/start bosildi: user_id=%s username=%s", user.id, user.username)

    caption = (
        f"Assalomu alaykum, {user.first_name}! \U0001F44B\n\n"
        "*Mudarris Akademiyasi*ga xush kelibsiz — Arab tili grammatikasini "
        "qiziqarli mashqlar orqali o'rganing.\n\n"
    )

    if os.path.exists(LOGO_PATH):
        with open(LOGO_PATH, "rb") as logo:
            await update.message.reply_photo(
                photo=logo,
                caption=caption,
                reply_markup=main_menu_keyboard(),
                parse_mode="Markdown",
            )
    else:
        logger.warning("image.png topilmadi (%s) — faqat matn yuborilmoqda", LOGO_PATH)
        await update.message.reply_text(
            caption,
            reply_markup=main_menu_keyboard(),
            parse_mode="Markdown",
        )


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Botda kutilmagan xatolik yuz berdi", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message is not None:
        try:
            await update.effective_message.reply_text(
                "Kechirasiz, xatolik yuz berdi. Birozdan so'ng qayta urinib ko'ring."
            )
        except Exception:
            logger.exception("Foydalanuvchiga xatolik xabarini yuborib bo'lmadi")


def register_handlers(app: Application) -> None:
    app.add_handler(CommandHandler("start", start_handler))
    app.add_error_handler(error_handler)
