from sqlalchemy import select, delete, update, not_
from sqlalchemy.ext.asyncio import AsyncSession


from database import Tracker


class TrackerRepo:
    def __init__(self, session: AsyncSession):
        self.__session = session

    async def add_tracker(self, query: str, chat_id: int):
        tracker = Tracker(chat_id=chat_id, query=query)


        self.__session.add(tracker)
        await self.__session.commit()

    async def remove_tracker(self, id: int):
        statement = delete(Tracker).where(Tracker.id == id)

        await self.__session.execute(statement)
        await self.__session.commit()

    async def get_trackers_by_chat_id(self, chat_id: int):
        statement = select(Tracker).where(Tracker.chat_id == chat_id)

        trackers = await self.__session.scalars(statement)
        return trackers.all()

    async def switch_status(self, id: int):
        statement = (update(Tracker).where(Tracker.id == id).values(status=not_(Tracker.status)).execution_options(synchronize_session="fetch"))

        await self.__session.execute(statement)
        await self.__session.commit()

    async def get_tracker_by_id(self, id: int):
        tracker = select(Tracker).where(Tracker.id == id)

        result = await self.__session.scalar(tracker)
        return result

    async def get_active_trackers(self):
        statement = select(Tracker).where(Tracker.status.is_(True))

        result = await self.__session.scalars(statement)
        return result.all()









