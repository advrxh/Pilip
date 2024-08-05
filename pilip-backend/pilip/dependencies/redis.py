from aioredis import Redis, RedisError
from fastapi import Request, HTTPException, status


async def get_redis(request: Request) -> Redis:

    return request.app.state.redis


async def redis_error_handler(request: Request, exception: RedisError):

    raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Redis error")
