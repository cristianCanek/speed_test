#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import sqlite3
import statistics

from database.database import CURRENT_SCHEMA_VERSION, DATABASE_FILE, get_schema_version


# ======================================================================================================================
# Exceptions.
# ======================================================================================================================

class DatabaseUnavailableError( RuntimeError ):
    """Raised when the persistent SQLite database cannot be read."""


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Connect to the SQLite database in read-only mode.
def _connect():
    try:
        conn = sqlite3.connect(
            f"file:{DATABASE_FILE}?mode=ro",
            uri=True
        )
        conn.row_factory = sqlite3.Row
        return conn

    except sqlite3.Error as err:
        raise DatabaseUnavailableError(
            f"Unable to open database '{DATABASE_FILE}': {err}"
        ) from None


# Convert a successful Version 2 database row to the public result format.
def _to_result( row ):
    if row is None:
        return None

    return {
        "timestamp":        row["timestamp_utc"],
        "download_mbps":    round( float( row["download_bandwidth_bytes_per_second"] ) / 1_000_000 * 8, 2 ),
        "upload_mbps":      round( float( row["upload_bandwidth_bytes_per_second"]   ) / 1_000_000 * 8, 2 ),
        "ping_ms":          float( row["ping_latency_ms"] ),
        "download_latency": float( row["download_latency_iqm_ms"] ),
        "upload_latency":   float( row["upload_latency_iqm_ms"] ),
        "result_url":       row["result_url"]
    }


# Add a timestamp threshold to a query when one was requested.
def _apply_threshold( query, threshold ):
    parameters = ()

    if threshold is not None:
        query += " AND julianday( timestamp_utc ) >= julianday( ? )"
        parameters = ( threshold, )

    return query, parameters


# Check if the Version 2 database is available for read access.
def database_is_available():
    try:
        with _connect() as conn:
            version = get_schema_version( conn )

            if version != CURRENT_SCHEMA_VERSION:
                return False

            conn.execute(
                "SELECT 1 FROM speedtest_runs LIMIT 1"
            ).fetchone()

        return True

    except ( DatabaseUnavailableError, sqlite3.Error ):
        return False


# Get the latest successful speed test result from the database.
def get_latest_result():
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT timestamp_utc,
                   download_bandwidth_bytes_per_second,
                   upload_bandwidth_bytes_per_second,
                   ping_latency_ms,
                   download_latency_iqm_ms,
                   upload_latency_iqm_ms,
                   result_url
            FROM   speedtest_runs
            WHERE  status = 'success'
            ORDER  BY timestamp_utc DESC
            LIMIT  1
            """
        ).fetchone()

    return _to_result( row )


# Get successful speed test results, optionally filtered by timestamp.
def get_results( threshold=None ):
    query = """
        SELECT timestamp_utc,
               download_bandwidth_bytes_per_second,
               upload_bandwidth_bytes_per_second,
               ping_latency_ms,
               download_latency_iqm_ms,
               upload_latency_iqm_ms,
               result_url
        FROM   speedtest_runs
        WHERE  status = 'success'
    """

    query, parameters = _apply_threshold( query, threshold )
    query += " ORDER BY timestamp_utc ASC"

    with _connect() as conn:
        rows = conn.execute( query, parameters ).fetchall()

    return [ _to_result( row ) for row in rows ]


# Count successful, failed and missing executions for a range.
def _get_execution_counts( threshold=None ):
    query = """
        SELECT status,
               COUNT(*) AS total
          FROM speedtest_runs
         WHERE 1 = 1
    """

    query, parameters = _apply_threshold( query, threshold )
    query += " GROUP BY status"

    counts = {
        "success": 0,
        "failed":  0,
        "missing": 0
    }

    with _connect() as conn:
        rows = conn.execute( query, parameters ).fetchall()

    for row in rows:
        counts[row["status"]] = int( row["total"] )

    return counts


# Get statistics for successful results and execution counts.
def get_statistics( threshold=None ):
    results = get_results( threshold )
    counts  = _get_execution_counts( threshold )

    base_statistics = {
        "samples":          len( results ),
        "total_executions": sum( counts.values() ),
        "successful_tests": counts["success"],
        "failed_tests":     counts["failed"],
        "missing_tests":    counts["missing"]
    }

    if len( results ) == 0:
        return {
            **base_statistics,
            "download_mbps": None,
            "upload_mbps": None,
            "ping_ms": None,
            "download_latency_ms": None,
            "upload_latency_ms": None
        }

    def summarize( key ):
        values = [ float( result[key] ) for result in results ]

        return {
            "average": round( statistics.fmean( values  ), 2 ),
            "median":  round( statistics.median( values ), 2 ),
            "minimum": round( min( values ), 2 ),
            "maximum": round( max( values ), 2 )
        }

    return {
        **base_statistics,
        "download_mbps":       summarize( "download_mbps"    ),
        "upload_mbps":         summarize( "upload_mbps"      ),
        "ping_ms":             summarize( "ping_ms"          ),
        "download_latency_ms": summarize( "download_latency" ),
        "upload_latency_ms":   summarize( "upload_latency"   )
    }
