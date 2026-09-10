from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def tracker_keyboard(tracker):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=("Stop" if tracker.status else "Start"), callback_data=f"status:{tracker.id}"),
            InlineKeyboardButton(text="Remove", callback_data=f"remove:{tracker.id}")]
        ]
    )
    return keyboard


