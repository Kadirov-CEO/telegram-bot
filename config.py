import os


def _require_env(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise RuntimeError(
            f"'{name}' environment variable topilmadi. "
            f"Hosting Dashboard > Variables bo'limida uni qo'shing."
        )
    return value


def _detect_public_url() -> str:
    # Qo'lda berilgan bo'lsa — shu ustun turadi.
    manual = os.environ.get("WEBHOOK_URL", "").rstrip("/")
    if manual:
        return manual

    # Railway: domen generatsiya qilingan bo'lsa, faqat hostname beradi (https:// yo'q).
    railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "").rstrip("/")
    if railway_domain:
        return "https://" + railway_domain

    # Render: to'liq https:// URL avtomatik beriladi.
    render_url = os.environ.get("RENDER_EXTERNAL_URL", "").rstrip("/")
    if render_url:
        return render_url

    return ""


class Config:
    # Majburiy: hosting platformasining Environment/Variables bo'limi orqali beriladi, koddan/fayldan emas.
    BOT_TOKEN: str = _require_env("BOT_TOKEN")

    # Web service HTTP so'rovlarni shu portda kutadi (Railway/Render buni avtomatik beradi).
    PORT: int = int(os.environ.get("PORT", "8080"))

    # WEBHOOK_URL qo'lda berilmasa, Railway/Render avtomatik domenidan foydalaniladi.
    # Hech biri topilmasa (masalan lokal kompyuterda ishga tushirilsa) — polling rejimiga o'tiladi.
    WEBHOOK_URL: str = _detect_public_url()

    # Ixtiyoriy qo'shimcha xavfsizlik qatlami: Telegram har bir webhook so'roviga shu tokenni
    # X-Telegram-Bot-Api-Secret-Token header'ida qo'shib yuboradi, biz uni tekshiramiz.
    WEBHOOK_SECRET: str = os.environ.get("WEBHOOK_SECRET", "")

    SITE_URL: str = os.environ.get("SITE_URL", "https://mudarris-akadmeiyasi.netlify.app/")
