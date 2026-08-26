#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron       import CronTrigger

from collector.collector import SpeedtestCollector

from config.settings import SettingsError, load_settings

from database.database import DatabaseMigrationError, ensure_database

from logging_config import configure_logging, get_logger


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Run the scheduler to execute Speedtests at the configured interval and timezone.
def run_scheduler( settings ):
    interval_minutes = settings["scheduler"]["interval_minutes"]
    timezone_name    = settings["scheduler"]["timezone"]

    cron_minute = (
        "0"
        if interval_minutes == 60
        else f"*/{interval_minutes}"
    )

    logger    = get_logger( "scheduler" )
    collector = SpeedtestCollector()
    scheduler = BlockingScheduler( timezone=timezone_name )

    scheduler.add_job(
        lambda             : collector.execute( save=True, source="scheduled" ),
        trigger            = CronTrigger( minute=cron_minute, second=0, timezone=timezone_name ),
        id                 = "speedtest",
        max_instances      = 1,
        coalesce           = True,
        misfire_grace_time = 30,
        replace_existing   = True
    )

    logger.info( "speed_test scheduler started." )
    logger.info( "Scheduled Speedtests every %s minute(s), aligned to the clock.", interval_minutes )
    logger.info( "Scheduler timezone: %s.", timezone_name )

    try:
        scheduler.start()
    except ( KeyboardInterrupt, SystemExit ):
        logger.info( "speed_test scheduler stopped." )


# Main entry point for the scheduler.
def main():
    configure_logging()
    logger = get_logger( "scheduler" )

    try:
        settings = load_settings()
        ensure_database()
        run_scheduler( settings )

    except ( SettingsError, DatabaseMigrationError ) as err:
        logger.error(
            "Collector startup aborted: %s",
            err
        )
        raise SystemExit( 1 ) from None


# ======================================================================================================================
# Main program.
# ======================================================================================================================

if __name__ == "__main__":
    main()
