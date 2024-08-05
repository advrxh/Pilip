from uuid import uuid4

from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status


from pilip.constants import Config
from pilip.models.auth import *
from pilip.dependencies.redis import get_redis

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login")
async def user_login(auth_in: Auth, redis: Redis = Depends(get_redis)):
    auth_in = auth_in.username, auth_in.password

    if auth_in in Config.AUTH_LIST:
        token = str(uuid4())

        await redis.rpush("tokens", token)

        return {"token": token}

    raise HTTPException(
        status.HTTP_400_BAD_REQUEST, detail="Username & Password not registered."
    )
