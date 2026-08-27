#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron         import CronTrigger

from collector.collector import SpeedtestCollector

from logging_config import get_logger


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Create the application scheduler without starting it.
#
# The scheduler lifecycle is owned by FastAPI in Alpha 8. Keeping construction
# separate from startup/shutdown makes the scheduler reusable and prevents a
# second standalone scheduler process from being required.
def create_scheduler( settings, collector=None ):
    interval_minutes = settings["scheduler"]["interval_minutes"]
    timezone_name    = settings["scheduler"]["timezone"]

    cron_minute = (
        "0"
        if interval_minutes == 60
        else f"*/{interval_minutes}"
    )

    logger    = get_logger( "scheduler" )
    collector = collector or SpeedtestCollector()

    scheduler = BackgroundScheduler( timezone=timezone_name )

    scheduler.add_job(
        lambda             : collector.execute( save=True, source="scheduled" ),
        trigger            = CronTrigger( minute=cron_minute, second=0, timezone=timezone_name ),
        id                 = "speedtest",
        max_instances      = 1,
        coalesce           = True,
        misfire_grace_time = 30,
        replace_existing   = True
    )

    logger.info( "Scheduler configured for every %s minute(s), aligned to the clock.", interval_minutes )
    logger.info( "Scheduler timezone: %s.", timezone_name )

    return scheduler
