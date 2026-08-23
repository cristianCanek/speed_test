#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from contextlib import asynccontextmanager
from pathlib    import Path

from fastapi             import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes      import router as api_router
from config.settings import SettingsError, load_settings


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

STATIC_DIR = Path( "/app/static" )


# ======================================================================================================================
# Application lifecycle.
# ======================================================================================================================

@asynccontextmanager
async def lifespan( app: FastAPI ):
    # Validate the shared application settings before accepting requests.
    # The collector remains responsible for creating and writing the SQLite
    # database during this milestone.
    try:
        load_settings()
    except SettingsError as err:
        raise RuntimeError( f"Unable to start speed_test application: {err}" ) from None

    yield


# ======================================================================================================================
# FastAPI application.
# ======================================================================================================================

app = FastAPI(
    title       = "speed_test API",
    description = "Public REST API for the speed_test Version 2 application.",
    version     = "2.0.0-alpha.5",
    lifespan    = lifespan
)

# API routes must be registered before mounting the frontend at "/".
app.include_router( api_router )

# The static frontend is served directly by FastAPI/Starlette.
app.mount(
    "/",
    StaticFiles( directory=STATIC_DIR, html=True ),
    name="frontend"
)
