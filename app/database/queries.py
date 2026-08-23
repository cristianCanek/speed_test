#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import sqlite3
import statistics

from database.database import DATABASE_FILE


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

# Convert a database row to a result dictionary.
def _to_result( row ):
    if row is None:
        return None

    return {
        "timestamp":        row["timestamp"],
        "download_mbps":    round( float( row["download_bandwith"] ) / 1_000_000 * 8, 2 ),
        "upload_mbps":      round( float( row["upload_bandwith"]   ) / 1_000_000 * 8, 2 ),
        "ping_ms":          float( row["ping_latency"] ),
        "download_latency": float( row["download_latency_iqm"] ),
        "upload_latency":   float( row["upload_latency_iqm"] ),
        "result_url":       row["result_url"]
    }


# Public query functions. ----------------------------------------------------------------------------------------------

# Check if the database is available for read access.
def database_is_available():
    try:
        with _connect() as conn:
            conn.execute( "SELECT 1" ).fetchone()

        return True

    except DatabaseUnavailableError:
        return False


# Get the latest speed test result from the database.
def get_latest_result():
    with _connect() as conn:
        row = conn.execute(
            """
            SELECT timestamp,
                   download_bandwith,
                   upload_bandwith,
                   ping_latency,
                   download_latency_iqm,
                   upload_latency_iqm,
                   result_url
              FROM rawResults
             ORDER BY datetime( timestamp ) DESC
             LIMIT 1
            """
        ).fetchone()

    return _to_result( row )


# Get all speed test results from the database, optionally filtered by a timestamp threshold.
def get_results( threshold=None ):
    query = """
        SELECT timestamp,
               download_bandwith,
               upload_bandwith,
               ping_latency,
               download_latency_iqm,
               upload_latency_iqm,
               result_url
          FROM rawResults
    """

    parameters = ()

    if threshold is not None:
        query += " WHERE julianday( timestamp ) >= julianday( ? )"
        parameters = ( threshold, )

    query += " ORDER BY datetime( timestamp ) ASC"

    with _connect() as conn:
        rows = conn.execute( query, parameters ).fetchall()

    return [ _to_result( row ) for row in rows ]


# Get statistics for the speed test results, optionally filtered by a timestamp threshold.
def get_statistics( threshold=None ):
    results = get_results( threshold )

    if len( results ) == 0:
        return {
            "samples": 0,
            "download_mbps": None,
            "upload_mbps": None,
            "ping_ms": None,
            "download_latency_ms": None,
            "upload_latency_ms": None,
            # Failed executions are not represented by the Version 1 schema.
            # Alpha 6 will make failures first-class database records.
            "failed_tests": None
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
        "samples":             len( results ),
        "download_mbps":       summarize( "download_mbps"    ),
        "upload_mbps":         summarize( "upload_mbps"      ),
        "ping_ms":             summarize( "ping_ms"          ),
        "download_latency_ms": summarize( "download_latency" ),
        "upload_latency_ms":   summarize( "upload_latency"   ),
        "failed_tests":        None
    }
