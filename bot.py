import logging

from telegram.ext import Application

from config import Config
from handlers import register_handlers
from logger import setup_logging

setup_logging()
logger = logging.getLogger(__name__)


def build_application() -> Application:
    application = Application.builder().token(Config.BOT_TOKEN).build()
    register_handlers(application)
    return application


def main() -> None:
    application = build_application()

    if Config.WEBHOOK_URL:
        # Production (Render): webhook rejimi. Render web service $PORT'ni tinglashni talab
        # qiladi, shuning uchun bu yerda polling emas, webhook ishlatiladi.
        webhook_path = Config.BOT_TOKEN
        full_webhook_url = f"{Config.WEBHOOK_URL}/{webhook_path}"
        logger.info("Webhook rejimida ishga tushmoqda: %s", full_webhook_url)
        application.run_webhook(
            listen="0.0.0.0",
            port=Config.PORT,
            url_path=webhook_path,
            webhook_url=full_webhook_url,
            secret_token=Config.WEBHOOK_SECRET or None,
        )
    else:
        # Lokal ishga tushirish / test uchun fallback (WEBHOOK_URL berilmagan bo'lsa).
        logger.info("WEBHOOK_URL topilmadi — polling rejimida ishga tushmoqda (faqat lokal test uchun).")
        application.run_polling()


if __name__ == "__main__":
    main()
