main_config = """
import uvicorn

from config.settings import *

app = app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=5000, reload=True, debug=True)
"""

constant = '''
from pydantic import BaseSettings

STATUS = "localhost"


class DbConfig(BaseSettings):
    """
        Handles the variables for database configuration
    """
    if STATUS == "localhost":
        POSTGRES_USER: str = ""
        POSTGRES_PASSWORD: str = ""
        POSTGRES_SERVER: str = ""
        POSTGRES_PORT: str = ""
        POSTGRES_DB: str = ""

    elif STATUS == "staging":
        POSTGRES_USER: str = ""
        POSTGRES_PASSWORD: str = ""
        POSTGRES_SERVER: str = ""
        POSTGRES_PORT: str = ""
        POSTGRES_DB: str = ""


config = DbConfig()
'''

settings = '''
"""
    This file includes all the configuration file for API
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Handles documentation title
app = FastAPI(
    version="",
    title="",
    description="",
    docs_url="/", redoc_url= None
)

# Handles cors
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
'''

requirements = '''
fastapi
uvicorn
'''