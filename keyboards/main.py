from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="+ Tracking")],
            [KeyboardButton(text="View tracker list")]
        ],
        resize_keyboard=True
    )
    return keyboard