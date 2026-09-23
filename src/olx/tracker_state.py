import asyncio
import logging

import redis.asyncio as redis
from os import getenv

from dotenv import load_dotenv

tracker_tasks: dict[int, asyncio.Task] = {}

load_dotenv()
host = str(getenv("REDIS_HOST"))
port = getenv("REDIS_PORT")

try:
    redis_client = redis.Redis(
        host=host,
        port=port,
        decode_responses=True
    )
except Exception as e:
    logging.error(f"Redis connection failed: {e}")