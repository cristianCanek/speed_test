#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from contextlib import asynccontextmanager
from pathlib    import Path

from fastapi             import FastAPI
from fastapi.staticfiles import StaticFiles

from api.routes          import router as api_router
from collector.scheduler import create_scheduler
from config.settings     import SettingsError, load_settings
from database.database   import DatabaseMigrationError, ensure_database
from logging_config      import configure_logging, get_logger


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

STATIC_DIR = Path( "/app/static" )


# ======================================================================================================================
# Application lifecycle.
# ======================================================================================================================

@asynccontextmanager
async def lifespan( app: FastAPI ):
    configure_logging()

    logger    = get_logger( "application" )
    scheduler = None

    try:
        # A single startup path now owns shared configuration, database
        # initialization/migrations, collector scheduling, REST API and frontend.
        settings = load_settings()
        ensure_database()

        scheduler = create_scheduler( settings )
        scheduler.start()

        # Keep the effective runtime configuration and scheduler available to
        # API routes without re-reading configuration independently.
        app.state.settings  = settings
        app.state.scheduler = scheduler

        logger.info( "speed_test application started." )
        get_logger( "scheduler" ).info( "speed_test scheduler started." )

        yield

    except ( SettingsError, DatabaseMigrationError ) as err:
        logger.error( "Application startup aborted: %s", err )
        raise RuntimeError( f"Unable to start speed_test application: {err}" ) from None

    finally:
        if scheduler is not None and scheduler.running:
            scheduler.shutdown( wait=False )
            get_logger( "scheduler" ).info( "speed_test scheduler stopped." )

        logger.info( "speed_test application stopped." )


# ======================================================================================================================
# FastAPI application.
# ======================================================================================================================

app = FastAPI(
    title       = "speed_test API",
    description = "Public REST API for the speed_test Version 2 application.",
    version     = "2.0.0-alpha.8",
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
