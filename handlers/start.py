from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main import main_keyboard

start_router = Router()


@start_router.message(Command("start"))
async def start(message: Message):
    await message.answer(
        f"Hello, this is olx parsing bot.",
        reply_markup=main_keyboard()
    )