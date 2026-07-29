import os


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"'{name}' environment variable topilmadi. "
            f"Render Dashboard > Environment bo'limida uni qo'shing."
        )
    return value


class Config:
    # Majburiy: Render Environment Variables orqali beriladi, koddan/fayldan emas.
    BOT_TOKEN: str = _require_env("BOT_TOKEN")

    # Render web service HTTP so'rovlarni shu portda kutadi (Render buni avtomatik beradi).
    PORT: int = int(os.environ.get("PORT", "8080"))

    # Render har bir web service uchun bu o'zgaruvchini avtomatik o'rnatadi
    # (masalan https://mudarris-akademiyasi-bot.onrender.com).
    RENDER_EXTERNAL_URL: str = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")

    # WEBHOOK_URL qo'lda berilmasa, RENDER_EXTERNAL_URL'dan foydalaniladi.
    # Ikkalasi ham bo'sh bo'lsa (masalan lokal kompyuterda ishga tushirilsa) — polling rejimiga o'tiladi.
    WEBHOOK_URL: str = (os.environ.get("WEBHOOK_URL", "").rstrip("/") or RENDER_EXTERNAL_URL)

    # Ixtiyoriy qo'shimcha xavfsizlik qatlami: Telegram har bir webhook so'roviga shu tokenni
    # X-Telegram-Bot-Api-Secret-Token header'ida qo'shib yuboradi, biz uni tekshiramiz.
    WEBHOOK_SECRET: str = os.environ.get("WEBHOOK_SECRET", "")

    SITE_URL: str = os.environ.get("SITE_URL", "https://mudarris-akadmeiyasi.netlify.app/")
