from telebot import types

import config

def main_keyboard():
    """Generates main keyboard for navigation."""

    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton('Бот для расчета', url = config.BOT_LINK))

    return keyboard