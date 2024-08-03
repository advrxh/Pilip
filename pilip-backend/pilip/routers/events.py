from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from fastapi import status as status_codes

from tortoise.queryset import QuerySet
from tortoise.exceptions import (
    DoesNotExist,
    IncompleteInstanceError,
    IntegrityError,
    OperationalError,
)


from pilip.models.event import *

router = APIRouter(prefix="/events")


@router.get("/")
async def get_events(
    id: int = None,
    status: Status = None,
):

    try:
        result_set = []

        if id is not None and status is None:
            result_set = await EventORM.get(id=id)

        elif id is None and status is not None:

            qualified_ids = [
                record.id for record in await EventStatusORM.all().filter(status=status)
            ]

            result_set = await EventORM.all().filter(id__in=qualified_ids)

        elif id is None and status is None:
            result_set = await EventORM.all()

        if isinstance(result_set, QuerySet):
            return Event.from_queryset(result_set)
        else:
            return result_set

    except DoesNotExist:
        return HTTPException(status_codes.HTTP_404_NOT_FOUND, "Not found.")


@router.put("/")
async def create_event(event: EventInput):

    try:
        result = await EventORM.create(**event.model_dump())
        await EventStatusORM.create(id=result.id)

        return result

    except IntegrityError or IncompleteInstanceError:
        return HTTPException(
            status_codes.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to update"
        )


@router.post("/")
async def update_event(id: int, event: EventInput):
    try:
        db_event = await EventORM.get(id=id)
        db_event.update_from_dict(event.model_dump())

        await db_event.save()

        return db_event

    except DoesNotExist:
        return HTTPException(status_codes.HTTP_404_NOT_FOUND, "Not found.")
    except IntegrityError or IncompleteInstanceError:
        return HTTPException(
            status_codes.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to update"
        )


@router.delete("/")
async def delete_event(id: int):

    try:
        event = await EventORM.get(id=id)
        event_status = await EventStatusORM.get(id=id)

        await event.delete()
        await event_status.delete()

        event.status = event_status

        return event

    except DoesNotExist:
        return HTTPException(status_codes.HTTP_404_NOT_FOUND, "Not found.")
    except OperationalError:
        return HTTPException(
            status_codes.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to delete"
        )


@router.get("/status")
async def get_event_status(id: int):
    try:
        result = await EventStatusORM.get(id=id)

        return result
    except DoesNotExist:
        return HTTPException(status_codes.HTTP_404_NOT_FOUND, "Not found.")


@router.post("/status")
async def update_event_status(id: int, status: Status):

    try:
        event_status = await EventStatusORM.get(id=id)
        event_status.status = status
        await event_status.save()

        return event_status

    except DoesNotExist:
        return HTTPException(status_codes.HTTP_404_NOT_FOUND, "Not found.")
    except IntegrityError or IncompleteInstanceError:
        return HTTPException(
            status_codes.HTTP_500_INTERNAL_SERVER_ERROR, "Unable to update"
        )
