#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import fcntl
import subprocess
import json
import sqlite3
import sys

from datetime import datetime, timezone

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron       import CronTrigger

from config.settings   import SettingsError, load_settings
from database.database import DATABASE_FILE, DatabaseMigrationError, ensure_database


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

# The command to perform the speed test.
SPEED_TEST_COMMAND = "/app/bin/speedtest --accept-license --accept-gdpr -f json-pretty";

# Lockfile to avoid running multiple speed tests at the same time.
LOCK_FILE = "/tmp/speed_test.lock"


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

class SpeedTest():

    def __init__( self, connector ):
        self.conn          = connector
        self.result        = {}
        self.error_type    = None
        self.error_message = None
        self.exit_code     = None


    def run( self ):
        try:
            output = subprocess.check_output(
                SPEED_TEST_COMMAND,
                shell  = True,
                text   = True,
                stderr = subprocess.STDOUT
            )

            self.result = json.loads( output )

        except subprocess.CalledProcessError as err:
            self.error_type    = "speedtest_cli_error"
            self.error_message = err.output.strip() if err.output else str( err )
            self.exit_code     = err.returncode

        except json.JSONDecodeError as err:
            self.error_type    = "invalid_json"
            self.error_message = str( err )


    def push( self ):
        if self.error_type is not None:
            insert_failed_run(
                self.conn,
                self.error_type,
                self.error_message,
                self.exit_code
            )

            print(
                f"Speedtest failed: {self.error_type}: {self.error_message}"
            )

            return

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
            normalize_utc_timestamp( self.result["timestamp"] ),
            self.result["type"],
            self.result["ping"]["jitter"],
            self.result["ping"]["latency"],
            self.result["ping"]["low"],
            self.result["ping"]["high"],
            self.result["download"]["bandwidth"],
            self.result["download"]["bytes"],
            self.result["download"]["elapsed"],
            self.result["download"]["latency"]["iqm"],
            self.result["download"]["latency"]["low"],
            self.result["download"]["latency"]["high"],
            self.result["download"]["latency"]["jitter"],
            self.result["upload"]["bandwidth"],
            self.result["upload"]["bytes"],
            self.result["upload"]["elapsed"],
            self.result["upload"]["latency"]["iqm"],
            self.result["upload"]["latency"]["low"],
            self.result["upload"]["latency"]["high"],
            self.result["upload"]["latency"]["jitter"],
            self.result["isp"],
            self.result["interface"]["internalIp"],
            self.result["interface"]["name"],
            self.result["interface"]["macAddr"],
            self.result["interface"]["isVpn"],
            self.result["interface"]["externalIp"],
            self.result["server"]["id"],
            self.result["server"]["host"],
            self.result["server"]["port"],
            self.result["server"]["name"],
            self.result["server"]["location"],
            self.result["server"]["country"],
            self.result["server"]["ip"],
            self.result["result"]["id"],
            self.result["result"]["url"],
            self.result["result"]["persisted"]
        )

        placeholders = ", ".join( ["?"] * len( values ) )

        query = (
            f"INSERT INTO speedtest_runs ( {columns} ) "
            f"VALUES ( {placeholders} )"
        )

        self.conn.execute( query, values )
        self.conn.commit()


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

def utc_now():
    return (
        datetime.now( timezone.utc )
        .isoformat( timespec="milliseconds" )
        .replace( "+00:00", "Z" )
    )


def normalize_utc_timestamp( timestamp ):
    parsed = datetime.fromisoformat( timestamp.replace( "Z", "+00:00" ) )

    return (
        parsed.astimezone( timezone.utc )
        .isoformat( timespec="milliseconds" )
        .replace( "+00:00", "Z" )
    )


def insert_failed_run( conn, error_type, error_message, exit_code=None ):
    conn.execute(
        """
        INSERT INTO speedtest_runs ( status, timestamp_utc, error_type, error_message, exit_code )
        VALUES ( 'failed', ?, ?, ?, ? )
        """,
        (
            utc_now(),
            error_type,
            error_message,
            exit_code
        )
    )

    conn.commit()


def insert_missing_run( conn, error_type, error_message ):
    conn.execute(
        """
        INSERT INTO speedtest_runs ( status, timestamp_utc, error_type, error_message )
        VALUES ( 'missing', ?, ?, ? )
        """,
        (
            utc_now(),
            error_type,
            error_message
        )
    )

    conn.commit()


# Run the speed test and push the result to the Version 2 database.
def run_speedtest():
    print( "Scheduled Speedtest triggered." )

    with open( LOCK_FILE, "w" ) as lock_file:
        try:
            fcntl.flock( lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB )
        except BlockingIOError:
            print( "Speedtest skipped: another Speedtest is already running." )

            conn = sqlite3.connect( DATABASE_FILE )

            try:
                insert_missing_run(
                    conn,
                    "overlap",
                    "Speedtest skipped because another execution already held the lock."
                )

            finally:
                conn.close()

            return

        conn = None

        try:
            conn = sqlite3.connect( DATABASE_FILE )

            speed_test = SpeedTest( conn )

            print( "Running Speedtest." )

            speed_test.run()
            speed_test.push()

        except sqlite3.Error as err:
            print( f"Database error: {err}" )

        finally:
            if conn is not None:
                conn.close()

            fcntl.flock( lock_file, fcntl.LOCK_UN )


# Run the speed test scheduler.
def run_scheduler( settings ):
    interval_minutes = settings["scheduler"]["interval_minutes"]
    timezone_name    = settings["scheduler"]["timezone"]

    # A 60-minute interval must run at minute zero. All other supported
    # intervals are divisors of 60 and therefore remain aligned to the clock.
    cron_minute = "0" if interval_minutes == 60 else f"*/{interval_minutes}"

    scheduler = BlockingScheduler( timezone=timezone_name )

    scheduler.add_job(
        run_speedtest,
        trigger            = CronTrigger( minute=cron_minute, second=0, timezone=timezone_name ),
        id                 = "speedtest",
        max_instances      = 1,
        coalesce           = True,
        misfire_grace_time = 30,
        replace_existing   = True,
    )

    print( "speed_test collector started." )
    print( f"Scheduled Speedtests every {interval_minutes} minute(s), aligned to the clock." )
    print( f"Scheduler timezone: {timezone_name}." )

    try:
        scheduler.start()
    except ( KeyboardInterrupt, SystemExit ):
        print( "speed_test collector stopped." )


# ======================================================================================================================
# Main program.
# ======================================================================================================================

if __name__ == "__main__":
    try:
        settings = load_settings()
        ensure_database()
        run_scheduler( settings )

    except ( SettingsError, DatabaseMigrationError ) as err:
        print( "", file=sys.stderr )
        print( "speed_test configuration error:", file=sys.stderr )
        print( f"  {err}", file=sys.stderr )
        print( "", file=sys.stderr )
        print( "Collector startup aborted.", file=sys.stderr )

        raise SystemExit( 1 ) from None
