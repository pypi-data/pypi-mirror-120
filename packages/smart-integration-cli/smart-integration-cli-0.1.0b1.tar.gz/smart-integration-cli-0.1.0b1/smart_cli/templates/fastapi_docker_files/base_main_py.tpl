import os
from importlib import import_module
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from .core import db
from .routers import api_router

settings = import_module(os.environ['FASTAPI_SETTINGS'])
app_type = import_module(os.environ['FASTAPI_APP_TYPE'])


app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version="0.1.1",
    openapi_url="/{{ params['project_name'] }}/openapi.json/",
    docs_url="/{{ params['project_name'] }}/docs/",
    redoc_url="/{{ params['project_name'] }}/redoc/",
)

db.connect()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.include_router(api_router, prefix=settings.API_PATH)