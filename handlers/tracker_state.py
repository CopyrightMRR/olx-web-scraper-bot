import asyncio
import redis.asyncio as redis

tracker_tasks: dict[int, asyncio.Task] = {}

redis_client = redis.Redis(
    host='localhost',
    port=6379,
    decode_responses=True
)