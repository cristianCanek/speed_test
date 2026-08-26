#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi           import APIRouter, HTTPException, Query, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from api.ranges          import RangeError, parse_range
from collector.collector import SpeedtestCollector
from config.settings     import load_settings
from database.queries    import DatabaseUnavailableError, database_is_available, get_latest_result, get_results, get_statistics


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

# The API router is used to register all the public endpoints for the speed_test application.
router = APIRouter()


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

class ManualTestRequest( BaseModel ):
    save: bool = True
    raw:  bool = False


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
    local_timezone  = ZoneInfo( timezone_name )
    now             = datetime.now( local_timezone )

    next_minute = ( ( now.minute // interval_minutes ) + 1 ) * interval_minutes

    if next_minute >= 60:
        boundary = (
            now.replace(
                minute=0,
                second=0,
                microsecond=0
            )
            + timedelta( hours=1 )
        )

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
        # The scheduled collector still runs in a separate container in Alpha 7.
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


# Endpoint for manually triggering a Speedtest execution.
@router.post(
    "/api/v1/tests/run",
    tags=["v1"],
    summary="Run a manual Speedtest"
)
def api_run_test( request: ManualTestRequest ):
    collector = SpeedtestCollector()

    outcome = collector.execute( save=request.save, source="api" )

    return outcome.to_dict( include_raw=request.raw )
