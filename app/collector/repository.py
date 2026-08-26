#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import sqlite3

from datetime import datetime, timezone

from collector.models  import SpeedtestMeasurement
from database.database import DATABASE_FILE


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

# Represents a repository for storing Ookla Speedtest measurements and execution outcomes in a SQLite database.
class SpeedtestRepository:
    def __init__( self, database_file=DATABASE_FILE ):
        self.database_file = database_file

    def _connect( self ):
        return sqlite3.connect( self.database_file )

    def save_success( self, measurement: SpeedtestMeasurement ):
        columns = """
            status,
            timestamp_utc,
            type,
            ping_jitter_ms,
            ping_latency_ms,
            ping_low_ms,
            ping_high_ms,
            download_bandwidth_bytes_per_second,
            download_bytes,
            download_elapsed_ms,
            download_latency_iqm_ms,
            download_latency_low_ms,
            download_latency_high_ms,
            download_latency_jitter_ms,
            upload_bandwidth_bytes_per_second,
            upload_bytes,
            upload_elapsed_ms,
            upload_latency_iqm_ms,
            upload_latency_low_ms,
            upload_latency_high_ms,
            upload_latency_jitter_ms,
            isp,
            interface_internal_ip,
            interface_name,
            interface_mac_address,
            interface_is_vpn,
            interface_external_ip,
            server_id,
            server_host,
            server_port,
            server_name,
            server_location,
            server_country,
            server_ip,
            result_id,
            result_url,
            result_persisted
        """

        values = (
            "success",
            measurement.timestamp_utc,
            measurement.type,
            measurement.ping_jitter_ms,
            measurement.ping_latency_ms,
            measurement.ping_low_ms,
            measurement.ping_high_ms,
            measurement.download_bandwidth_bytes_per_second,
            measurement.download_bytes,
            measurement.download_elapsed_ms,
            measurement.download_latency_iqm_ms,
            measurement.download_latency_low_ms,
            measurement.download_latency_high_ms,
            measurement.download_latency_jitter_ms,
            measurement.upload_bandwidth_bytes_per_second,
            measurement.upload_bytes,
            measurement.upload_elapsed_ms,
            measurement.upload_latency_iqm_ms,
            measurement.upload_latency_low_ms,
            measurement.upload_latency_high_ms,
            measurement.upload_latency_jitter_ms,
            measurement.isp,
            measurement.interface_internal_ip,
            measurement.interface_name,
            measurement.interface_mac_address,
            int( measurement.interface_is_vpn ),
            measurement.interface_external_ip,
            measurement.server_id,
            measurement.server_host,
            measurement.server_port,
            measurement.server_name,
            measurement.server_location,
            measurement.server_country,
            measurement.server_ip,
            measurement.result_id,
            measurement.result_url,
            int( measurement.result_persisted )
        )

        placeholders = ", ".join( ["?"] * len( values ) )

        query = ( f"INSERT INTO speedtest_runs ( {columns} ) VALUES ( {placeholders} )" )

        with self._connect() as conn:
            conn.execute( query, values )
            conn.commit()

    def save_failed( self, error_type, error_message, exit_code=None ):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO speedtest_runs ( status, timestamp_utc, error_type, error_message, exit_code )
                VALUES ( 'failed', ?, ?, ?, ? )
                """,
                ( utc_now(), error_type, error_message, exit_code )
            )
            conn.commit()

    def save_missing( self, error_type, error_message ):
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO speedtest_runs ( status, timestamp_utc, error_type, error_message )
                VALUES ( 'missing', ?, ?, ? )
                """,
                ( utc_now(), error_type, error_message )
            )
            conn.commit()


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Returns the current UTC timestamp in ISO 8601 format with milliseconds precision and 'Z' suffix.
def utc_now():
    return (
        datetime.now( timezone.utc )
        .isoformat( timespec="milliseconds" )
        .replace( "+00:00", "Z" )
    )