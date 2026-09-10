from aiogram import Dispatcher

from middlewares.session import DatabaseSessionMiddleware

async def register_middleware(dispatcher: Dispatcher, session_maker):
    dispatcher.update.middleware(DatabaseSessionMiddleware(session_maker))