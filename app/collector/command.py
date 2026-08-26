#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import argparse
import json

from collector.collector import SpeedtestCollector
from config.settings     import SettingsError, load_settings
from database.database   import DatabaseMigrationError, ensure_database
from logging_config      import configure_logging, get_logger


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Build the command line argument parser for the collector command line interface.
def _build_parser():
    parser = argparse.ArgumentParser(
        prog        = "python -m collector",
        description = "speed_test collector command line interface."
    )

    subparsers = parser.add_subparsers(
        dest     = "command",
        required = True
    )

    run_parser = subparsers.add_parser(
        "run",
        help = "Run one manual Speedtest."
    )

    run_parser.add_argument(
        "--save",
        action = "store_true",
        help   = "Persist the manual execution in the SQLite database."
    )

    run_parser.add_argument(
        "--raw-json",
        action = "store_true",
        help = (
            "Print only the raw Ookla JSON payload to stdout. "
            "Diagnostic logs continue on stderr and in collector.log."
        )
    )

    return parser


# Run a manual Speedtest and print the results to stdout.
def run_manual( args ):
    configure_logging()
    load_settings()

    if args.save:
        ensure_database()

    collector = SpeedtestCollector()

    outcome = collector.execute(
        save   = args.save,
        source = "manual"
    )

    if args.raw_json and outcome.raw_output:
        print( outcome.raw_output.rstrip() )
    else:
        print( json.dumps( outcome.to_dict( include_raw=False ), indent=2 ) )

    return (
        0
        if outcome.status.value == "success"
        else 1
    )


# Main entry point for the collector command line interface.
def main( argv=None ):
    configure_logging()
    logger = get_logger( "collector" )

    parser = _build_parser()
    args   = parser.parse_args( argv )

    try:
        if args.command == "run":
            return run_manual( args )

    except ( SettingsError, DatabaseMigrationError ) as err:
        logger.error( "Collector command failed: %s", err )
        return 2

    parser.error( "Unknown collector command." )


# ======================================================================================================================
# Main program.
# ======================================================================================================================

if __name__ == "__main__":
    raise SystemExit( main() )
