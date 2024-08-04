from contextlib import asynccontextmanager

import aioredis
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from tortoise.contrib.fastapi import register_tortoise

load_dotenv()

from pilip.constants import Config
from pilip.routers import events_router, submissions_router
from pilip.dependencies.redis import redis_error_handler


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.redis = await aioredis.from_url(
        url="redis://localhost", username="root", password="root"
    )
    yield
    await app.state.redis.close()


app = FastAPI(debug=Config.DEBUG, title="Pilip", lifespan=lifespan)

# exceptions
app.add_exception_handler(aioredis.RedisError, redis_error_handler)

# setup routers
app.include_router(events_router)
app.include_router(submissions_router)


@app.get("/")
async def root(request: Request):
    return f"UPTIME: {Config.since_startup()}"


register_tortoise(
    app,
    db_url=Config.DB_URL,
    modules={"models": ["pilip.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
