from aiogram import Router, F, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery
from database.repositories.tracker import TrackerRepo
from handlers.tracker_state import tracker_tasks
from handlers.tracking import create_task
from keyboards.tracker import tracker_keyboard
import asyncio



list_router = Router()


async def stop_tracker(tracker):
    task = tracker_tasks.pop(tracker.id, None)

    if task:
        task.cancel()
        try:
            await task
        except asyncio.CancelledError:
            pass


@list_router.message(F.text.lower() == "view tracker list")
async def tracker_list_cmd(message: Message, tracker_repo: TrackerRepo):
    trackers = await tracker_repo.get_trackers_by_chat_id(message.chat.id)
    if not trackers:
        await message.answer("No trackers found")
        return

    for tracker in trackers:
            await message.answer(
                f"📎 <b>ID:</b> <code>{tracker.id}</code>\n"
                f"📌 <b>Query:</b> <code>{tracker.query}</code>\n",
                parse_mode="HTML",
                reply_markup=tracker_keyboard(tracker)
            )


@list_router.callback_query(F.data.startswith("remove:"))
async def tracker_remove(callback: CallbackQuery, tracker_repo: TrackerRepo):
    id = int(callback.data.split(":")[1])
    await tracker_repo.remove_tracker(id=id)
    await callback.message.delete()


@list_router.callback_query(F.data.startswith("status:"))
async def pick_tracker_status(callback: CallbackQuery, tracker_repo: TrackerRepo, bot: Bot):
    id = int(callback.data.split(":")[1])
    tracker = await tracker_repo.get_tracker_by_id(id)

    if not tracker.status:
        await create_task(bot, tracker)
    else:
        await stop_tracker(tracker)

    await tracker_repo.switch_status(id)
    updated_tracker = await tracker_repo.get_tracker_by_id(id)

    try:
        await callback.message.edit_reply_markup(reply_markup=tracker_keyboard(updated_tracker))
    except TelegramBadRequest as e:
        if "message is not modified" not in str(e):
            raise
    await callback.answer()