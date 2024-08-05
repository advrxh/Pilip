from contextlib import asynccontextmanager

from aioredis import Redis, RedisError, from_url
from fastapi import FastAPI, Request, Depends
from tortoise.contrib.fastapi import register_tortoise


from pilip.constants import Config
from pilip.routers import events_router, submissions_router, auth_router
from pilip.dependencies.redis import get_redis, redis_error_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await from_url(url=Config.REDIS_URL)

    await app.state.redis.rpush("tokens", "0")
    await app.state.redis.expire("tokens", 24 * 60 * 60)
    yield
    await app.state.redis.close()


app = FastAPI(debug=Config.DEBUG, title="Pilip", lifespan=lifespan)

# exceptions
app.add_exception_handler(RedisError, redis_error_handler)

# setup routers
app.include_router(events_router)
app.include_router(submissions_router)
app.include_router(auth_router)


@app.get("/")
async def root(request: Request, redis: Redis = Depends(get_redis)):
    return f"UPTIME: {Config.since_startup()}"


register_tortoise(
    app,
    db_url=Config.DB_URL,
    modules={"models": ["pilip.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
