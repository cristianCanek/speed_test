#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from pydantic import BaseModel

from api.ranges import RangeError, parse_range

from collector.collector import SpeedtestCollector

from database.queries import DatabaseUnavailableError, database_is_available, get_latest_result, get_results, get_statistics

from fastapi           import APIRouter, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse


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

# Helper function to raise a 503 Service Unavailable error when the database is unavailable.
def _http_database_error( err ):
    raise HTTPException( status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str( err ) ) from None


# This function is used to validate the "range" query parameter in the API endpoints.
def _parse_range_or_400( range_value ):
    try:
        return parse_range( range_value )
    except RangeError as err:
        raise HTTPException( status_code=status.HTTP_400_BAD_REQUEST, detail=str( err ) ) from None


# Helper function to retrieve the current runtime settings from the FastAPI request object.
def _runtime_settings( request: Request ):
    return request.app.state.settings


# Helper function to retrieve the current scheduler state from the FastAPI request object.
def _scheduler_state( request: Request ):
    scheduler = request.app.state.scheduler
    job       = scheduler.get_job( "speedtest" )

    return {
        "status": (
            "running"
            if scheduler.running
            else "stopped"
        ),
        "next_scheduled_boundary": (
            job.next_run_time.isoformat()
            if job is not None and job.next_run_time is not None
            else None
        )
    }


# ======================================================================================================================
# Public API.
# ======================================================================================================================

# Endpoint for monitoring the health of the application and its database connection.
# Returns a 200 OK status if the application is healthy, or a 503 Service Unavailable
# status if the database is unavailable.
@router.get( "/health", tags=["health"], summary="Application health" )
def health( request: Request ):
    database_ok  = database_is_available()
    scheduler    = request.app.state.scheduler
    scheduler_ok = scheduler is not None and scheduler.running
    healthy      = database_ok and scheduler_ok

    payload = {
        "status": (
            "healthy"
            if healthy
            else "degraded"
        ),
        "database": (
            "ok"
            if database_ok
            else "unavailable"
        ),
        "scheduler": (
            "running"
            if scheduler_ok
            else "stopped"
        )
    }

    return JSONResponse(
        content=payload,
        status_code=(
            status.HTTP_200_OK
            if healthy
            else status.HTTP_503_SERVICE_UNAVAILABLE
        )
    )


# Endpoint for retrieving the current application and measurement status.
@router.get( "/api/v1/status", tags=["v1"], summary="Current application and measurement status" )
def api_status( request: Request ):
    settings        = _runtime_settings( request )
    scheduler_state = _scheduler_state(  request )

    try:
        latest_result = get_latest_result()

    except DatabaseUnavailableError as err:
        _http_database_error( err )

    return {
        "application": "running",
        "collector_status": "integrated",
        "scheduler": {
            "status": scheduler_state["status"],
            "interval_minutes": settings["scheduler"]["interval_minutes"],
            "timezone": settings["scheduler"]["timezone"],
            "next_scheduled_boundary": scheduler_state["next_scheduled_boundary"]
        },
        "last_result": latest_result
    }


# Endpoint for retrieving historical Speedtest results, optionally filtered by a time range.
@router.get( "/api/v1/results", tags=["v1"], summary="Historical Speedtest results" )
def api_results( range_value: str = Query( default="24h", alias="range", description="Examples: 24h, 7d, 30d, 365d, all" ) ):
    threshold = _parse_range_or_400( range_value )

    try:
        results = get_results( threshold )
    except DatabaseUnavailableError as err:
        _http_database_error( err )

    return {
        "range"   : range_value,
        "count"   : len( results ),
        "results" : results
    }


# Endpoint for retrieving basic statistics for Speedtest results, optionally filtered
# by a time range.
@router.get( "/api/v1/statistics", tags=["v1"], summary="Basic statistics for a result range" )
def api_statistics( range_value: str = Query( default="24h", alias="range", description="Examples: 24h, 7d, 30d, 365d, all"  ) ):
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
@router.get( "/api/v1/config", tags=["v1"], summary="Public application configuration" )
def api_config( request: Request ):
    settings = _runtime_settings( request )

    # Only non-sensitive application settings are exposed here.
    return {
        "scheduler": {
            "interval_minutes": settings["scheduler"]["interval_minutes"],
            "timezone": settings["scheduler"]["timezone"]
        }
    }


# Endpoint for manually triggering a Speedtest execution.
@router.post( "/api/v1/tests/run", tags=["v1"], summary="Run a manual Speedtest" )
def api_run_test( request_data: ManualTestRequest ):
    collector = SpeedtestCollector()
    outcome   = collector.execute( save=request_data.save, source="api" )

    return outcome.to_dict( include_raw=request_data.raw )
