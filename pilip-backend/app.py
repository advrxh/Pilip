from datetime import datetime

from fastapi import FastAPI
from tortoise.contrib.fastapi import HTTPNotFoundError, register_tortoise
from dotenv import load_dotenv

load_dotenv()

from pilip.constants import Config
from pilip.routers import events_router


app = FastAPI(debug=Config.DEBUG, title="Pilip")
app.include_router(events_router)


@app.on_event("startup")
async def startup():
    Config.STARTUP = datetime.now()


@app.get("/")
async def root():
    return f"UPTIME: {Config.since_startup()}"


register_tortoise(
    app,
    db_url=Config.DB_URL,
    modules={"models": ["pilip.models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
