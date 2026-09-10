import asyncio
import logging

from aiogram import Dispatcher, Bot
from os import getenv
from database import session_maker, engine
from database.models import BaseModel
from database.repositories.tracker import TrackerRepo
from handlers.start import start_router
from handlers.tracking import router, create_task
from handlers.tracking_list import list_router
from middlewares import register_middleware
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s | %(message)s"
)
logger = logging.getLogger(__name__)

load_dotenv()
token = getenv("BOT_TOKEN")

routers = [
    router,
    list_router,
    start_router
]

if not token:
    raise ValueError("Bot token not provided")

bot = Bot(token=token)


dispatcher = Dispatcher()

dispatcher.include_routers(*routers)

async def init_models(e):
    async with e.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

async def main():
    try:

        await register_middleware(dispatcher, session_maker)
        await init_models(engine)

        async with session_maker() as session:
            tracker_repo = TrackerRepo(session)

            trackers = await tracker_repo.get_active_trackers()

        for tracker in trackers:
            await create_task(bot, tracker)

        await dispatcher.start_polling(bot)

    except Exception:

        logger.exception("Bot didn't started because of any problems")
        raise

    finally:
        await bot.session.close()


if __name__ == "__main__":
    asyncio.run(main())