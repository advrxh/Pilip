from aioredis import Redis
from fastapi import APIRouter, Depends


from pilip.dependencies.redis import get_redis
from pilip.models.submission import *
from pilip.util import load_from_str, dump_to_str

router = APIRouter(prefix="/submissions")


@router.put("/{event_id}")
async def create_submission(
    event_id: int,
    user_id: int,
    submission: Submission,
    redis: Redis = Depends(get_redis),
):

    user_id = str(user_id)
    event_id = str(event_id)

    all_submissions = await redis.get(event_id)
    all_submissions = load_from_str(all_submissions)

    if all_submissions is None:
        user_submissions = [submission.model_dump()]
        await redis.set(event_id, dump_to_str({user_id: user_submissions}))

        return user_submissions

    user_submissions = all_submissions.get(user_id)

    if user_submissions is None:
        user_submissions = [submission.model_dump()]
    else:
        user_submissions.append(submission.model_dump())

    all_submissions[user_id] = user_submissions

    await redis.set(event_id, dump_to_str(all_submissions))

    return user_submissions


@router.get("/{event_id}")
async def get_submissions_by_event(
    event_id: int, user_id: int = None, redis: Redis = Depends(get_redis)
):

    event_id = str(event_id) if event_id is not None else event_id
    user_id = str(user_id) if user_id is not None else user_id

    all_submissions = await redis.get(event_id)
    all_submissions = load_from_str(all_submissions)
    all_submissions = {} if all_submissions is None else all_submissions

    user_submissions = all_submissions.get(user_id, [])

    if user_id is None:
        return all_submissions
    return user_submissions


@router.post("/{event_id}")
async def update_submission_by_user(
    event_id: int,
    user_id: int,
    submissions: List[Submission] = [],
    redis: Redis = Depends(get_redis),
):
    pass
