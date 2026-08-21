#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import fcntl
import subprocess
import json
import sqlite3
import sys

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron       import CronTrigger

from config.settings                 import SettingsError, load_settings
from database.database               import DATABASE_FILE, ensure_database


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
        self.conn = connector;
        self.result = {};
        self.lastSpeedtestWithError = False;
    
    def run( self ):
        try:
            self.result = json.loads( subprocess.check_output( SPEED_TEST_COMMAND, shell=True, text=True ) );
        except subprocess.CalledProcessError as e:
            self.lastSpeedtestWithError = True;
            print( f"Error executing command: {e}" );

    def push( self ):
        if( self.lastSpeedtestWithError == False ):
            STR_COLUMNS = """
                type,
                timestamp,
                ping_jitter,
                ping_latency,
                ping_low,
                ping_high,
                download_bandwith,
                download_bytes,
                download_elapsed,
                download_latency_iqm,
                download_latency_low,
                download_latency_high,
                download_latency_jitter,
                upload_bandwith,
                upload_bytes,
                upload_elapsed,
                upload_latency_iqm,
                upload_latency_low,
                upload_latency_high,
                upload_latency_jitter,
                isp,
                interface_internalIp,
                interface_name,
                interface_macAddr,
                interface_isVpn,
                interface_externalIp,
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
            
            STR_VALUES = (
                self.result["type"],
                self.result["timestamp"],
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
            );

            placeholders = ", ".join( ["?"] * len( STR_VALUES ) )

            STR_INSERT = f"INSERT INTO rawResults( {STR_COLUMNS} ) VALUES( {placeholders} )";

            try:
                cur = self.conn.cursor();
                cur.execute( STR_INSERT, STR_VALUES );
                self.conn.commit();
            except sqlite3.Error as err:
                print( err );


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Run the speed test and push the results to the database.
def run_speedtest():
    print( "Scheduled Speedtest triggered." )
    with open( LOCK_FILE, "w" ) as lock_file:
        try:
            fcntl.flock( lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB )
        except BlockingIOError:
            print( "Speedtest skipped: another Speedtest is already running." )
            return

        conn = None

        try:
            conn = sqlite3.connect( DATABASE_FILE )
            speedTest = SpeedTest( conn )
            print("Running Speedtest.")
            speedTest.run()
            speedTest.push()
        except sqlite3.Error as err:
            print( err )
        finally:
            if conn is not None:
                conn.close()
            fcntl.flock( lock_file, fcntl.LOCK_UN )

# Run the speed test scheduler.
def run_scheduler( settings ):
    interval_minutes = settings["scheduler"]["interval_minutes"]
    timezone         = settings["scheduler"]["timezone"]

    # A 60-minute interval must run at minute zero. All other supported
    # intervals are divisors of 60 and therefore remain aligned to the clock.
    cron_minute = "0" if interval_minutes == 60 else f"*/{interval_minutes}"

    scheduler = BlockingScheduler( timezone=timezone )

    scheduler.add_job(
        run_speedtest,
        trigger            = CronTrigger( minute=cron_minute, second=0, timezone=timezone ),
        id                 = "speedtest",
        max_instances      = 1,
        coalesce           = True,
        misfire_grace_time = 30,
        replace_existing   = True,
    )

    print( "speed_test collector started." )
    print( f"Scheduled Speedtests every {interval_minutes} minute(s), aligned to the clock." )
    print( f"Scheduler timezone: {timezone}." )

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

    except SettingsError as err:
        print( "", file=sys.stderr )
        print( "speed_test configuration error:", file=sys.stderr )
        print( f"  {err}", file=sys.stderr )
        print( "", file=sys.stderr )
        print( "Collector startup aborted.", file=sys.stderr )

        raise SystemExit( 1 ) from None
