from aioredis import Redis
from fastapi import APIRouter, Depends, status, HTTPException


from pilip.dependencies.redis import get_redis
from pilip.models.submission import *
from pilip.util import load_from_str, dump_to_str, get_new_submission_id

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
        user_submissions = {0: submission.model_dump()}
        await redis.set(event_id, dump_to_str({user_id: user_submissions}))

        return user_submissions

    user_submissions = all_submissions.get(user_id)

    if user_submissions is None:
        user_submissions = {0: submission.model_dump()}
    else:
        submission_id = get_new_submission_id(user_submissions)

        user_submissions[submission_id] = submission.model_dump()

    all_submissions[user_id] = user_submissions

    await redis.set(event_id, dump_to_str(all_submissions))

    return user_submissions


@router.get("/{event_id}")
async def get_submissions_by_event(
    event_id: int,
    user_id: int = None,
    submission_id: int = None,
    redis: Redis = Depends(get_redis),
):

    event_id = str(event_id) if event_id is not None else event_id
    user_id = str(user_id) if user_id is not None else user_id
    submission_id = str(submission_id) if user_id is not None else submission_id

    all_submissions = await redis.get(event_id)
    all_submissions = load_from_str(all_submissions)

    if all_submissions is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Event not found.")

    user_submissions = all_submissions.get(user_id)

    if user_submissions is None:
        return HTTPException(
            status.HTTP_404_NOT_FOUND, detail="User not found. Create an event first."
        )

    submission = user_submissions.get(submission_id)

    if submission is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Submission not found.")

    return submission


@router.post("/{event_id}")
async def update_submission_by_user(
    event_id: int,
    user_id: int,
    submission_id: int,
    submission: Submission,
    redis: Redis = Depends(get_redis),
):
    event_id = str(event_id) if event_id is not None else event_id
    user_id = str(user_id) if user_id is not None else user_id
    submission_id = str(submission_id) if user_id is not None else submission_id

    all_submissions = await redis.get(event_id)
    all_submissions = load_from_str(all_submissions)

    if all_submissions is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Event not found.")

    user_submissions = all_submissions.get(user_id)

    if user_submissions is None:
        return HTTPException(
            status.HTTP_404_NOT_FOUND, detail="User not found. Create an event first."
        )

    user_submission = user_submissions.get(submission_id)

    if user_submission is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Submission not found.")

    user_submissions[submission_id] = submission.model_dump()
    all_submissions[user_id] = user_submissions

    await redis.set(event_id, dump_to_str(all_submissions))

    return submission


@router.delete("/{event_id}")
async def delete_submission_by_user(
    event_id: int,
    user_id: int,
    submission_id: int,
    redis: Redis = Depends(get_redis),
):
    event_id = str(event_id) if event_id is not None else event_id
    user_id = str(user_id) if user_id is not None else user_id
    submission_id = str(submission_id) if user_id is not None else submission_id

    all_submissions = await redis.get(event_id)
    all_submissions = load_from_str(all_submissions)

    if all_submissions is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Event not found.")

    user_submissions = all_submissions.get(user_id)

    if user_submissions is None:
        return HTTPException(
            status.HTTP_404_NOT_FOUND,
            detail="Submissions not found. Make a submission first.",
        )

    user_submission = user_submissions.get(submission_id)

    if user_submission is None:
        return HTTPException(status.HTTP_404_NOT_FOUND, detail="Submission not found.")

    submission = user_submissions[submission_id]

    del user_submissions[submission_id]
    all_submissions[user_id] = user_submissions

    await redis.set(event_id, dump_to_str(all_submissions))

    return submission
