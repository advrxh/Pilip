import os
from datetime import datetime


class Config:
    DEBUG = os.getenv("DEBUG", "false") == "true"
    STARTUP = datetime.now()
    DB_URL = os.getenv("DB_URL")

    def since_startup():
        duration = datetime.now() - Config.STARTUP

        return f"{round(duration.seconds/60)} minutes."
