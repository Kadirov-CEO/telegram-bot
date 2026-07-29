from telegram import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

from config import Config


def main_menu_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("📚 Ilovani ochish", web_app=WebAppInfo(url=Config.SITE_URL)),
    ]])
