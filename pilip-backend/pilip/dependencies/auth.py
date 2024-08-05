from typing_extensions import Annotated

from aioredis import Redis
from fastapi import Request, Depends, HTTPException, status, Header

from pilip.dependencies.redis import get_redis


async def check_authorization(
    x_token: Annotated[str, Header()], redis: Redis = Depends(get_redis)
):

    if x_token is None:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Not authorized.")

    token_list = await redis.lrange("tokens", 0, -1)
    token_list = [token.decode("utf-8") for token in token_list]

    if x_token not in token_list:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail="Invalid auth token.")
