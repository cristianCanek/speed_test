#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi           import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse

from api.ranges       import RangeError, parse_range
from config.settings  import load_settings
from database.queries import DatabaseUnavailableError, database_is_available, get_latest_result, get_results, get_statistics


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

# The API router is used to register all the public endpoints for the speed_test application.
router = APIRouter()


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Helper functions for the API endpoints.
def _http_database_error( err ):
    raise HTTPException(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        detail=str( err )
    ) from None


# Helper function to parse an API range or raise a 400 Bad Request error.
def _parse_range_or_400( range_value ):
    try:
        return parse_range( range_value )
    except RangeError as err:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str( err )
        ) from None


# Helper function to calculate the next scheduled boundary for the Speedtest scheduler.
def _next_schedule_boundary( interval_minutes, timezone_name ):
    tz  = ZoneInfo( timezone_name )
    now = datetime.now( tz )

    minutes_from_hour = now.minute
    next_minute = ( ( minutes_from_hour // interval_minutes ) + 1 ) * interval_minutes

    if next_minute >= 60:
        boundary = now.replace(
            minute=0,
            second=0,
            microsecond=0
        ) + timedelta( hours=1 )
    else:
        boundary = now.replace(
            minute=next_minute,
            second=0,
            microsecond=0
        )

    return boundary.isoformat()


# ======================================================================================================================
# Version 1 API.
# ======================================================================================================================

# Endpoint for monitoring the health of the application and its database connection.
# Returns a 200 OK status if the application is healthy, or a 503 Service Unavailable
# status if the database is unavailable.
@router.get(
    "/health",
    tags=["health"],
    summary="Application health"
)
def health():
    database_ok = database_is_available()

    payload = {
        "status":   "healthy" if database_ok else "degraded",
        "database": "ok"      if database_ok else "unavailable"
    }

    return JSONResponse(
        content=payload,
        status_code=(
            status.HTTP_200_OK
            if database_ok
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
    )


# Endpoint for retrieving the current application and measurement status.
@router.get(
    "/api/v1/status",
    tags=["v1"],
    summary="Current application and measurement status"
)
def api_status():
    settings = load_settings()

    interval_minutes = settings["scheduler"]["interval_minutes"]
    timezone_name    = settings["scheduler"]["timezone"]

    try:
        latest_result = get_latest_result()
    except DatabaseUnavailableError as err:
        _http_database_error( err )

    return {
        "application": "running",
        # The collector remains a separate container in Alpha 5, so FastAPI
        # cannot truthfully report its live process state yet.
        "collector_status": "external",
        "scheduler": {
            "interval_minutes": interval_minutes,
            "timezone": timezone_name,
            "next_scheduled_boundary": _next_schedule_boundary(
                interval_minutes,
                timezone_name
            )
        },
        "last_result": latest_result
    }


# Endpoint for retrieving historical Speedtest results, optionally filtered by a time range.
@router.get(
    "/api/v1/results",
    tags=["v1"],
    summary="Historical Speedtest results"
)
def api_results(
    range_value: str = Query(
        default="24h",
        alias="range",
        description="Examples: 24h, 7d, 30d, 365d, all"
    )
):
    threshold = _parse_range_or_400( range_value )

    try:
        results = get_results( threshold )
    except DatabaseUnavailableError as err:
        _http_database_error( err )

    return {
        "range": range_value,
        "count": len( results ),
        "results": results
    }


# Endpoint for retrieving basic statistics for Speedtest results, optionally filtered
# by a time range.
@router.get(
    "/api/v1/statistics",
    tags=["v1"],
    summary="Basic statistics for a result range"
)
def api_statistics(
    range_value: str = Query(
        default="24h",
        alias="range",
        description="Examples: 24h, 7d, 30d, 365d, all"
    )
):
    threshold = _parse_range_or_400( range_value )

    try:
        statistics_data = get_statistics( threshold )
    except DatabaseUnavailableError as err:
        _http_database_error( err )

    return {
        "range": range_value,
        **statistics_data
    }


# Endpoint for retrieving the public application configuration, excluding sensitive information.
@router.get(
    "/api/v1/config",
    tags=["v1"],
    summary="Public application configuration"
)
def api_config():
    settings = load_settings()

    # Only non-sensitive application settings are exposed here.
    return {
        "scheduler": {
            "interval_minutes": settings["scheduler"]["interval_minutes"],
            "timezone": settings["scheduler"]["timezone"]
        }
    }


# Endpoint for manually triggering a Speedtest execution. This endpoint is reserved
# for the v1 API and will be implemented in v2.0.0-alpha.7 after the collector becomes
# reusable application code.
@router.post(
    "/api/v1/tests/run",
    tags=["v1"],
    summary="Run a manual Speedtest",
    status_code=status.HTTP_501_NOT_IMPLEMENTED
)
def api_run_test():
    # Reserved now so the public API shape is visible from Alpha 5.
    # Actual execution belongs to the collector refactor in Alpha 7. Calling
    # docker exec or exposing the Docker socket here would create the wrong
    # coupling between the application and collector containers.
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail=(
            "Manual Speedtest execution is reserved by the v1 API but will "
            "be implemented in v2.0.0-alpha.7 after the collector becomes "
            "reusable application code."
        )
    )
