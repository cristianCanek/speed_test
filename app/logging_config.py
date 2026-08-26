#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import logging
import sys
import time

from pathlib import Path


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

LOG_DIR            = Path( "/config/logs" )
COLLECTOR_LOG_FILE = LOG_DIR / "collector.log"
ROOT_LOGGER_NAME   = "speed_test"


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Configure the logging for the collector module.
def configure_logging( log_file=COLLECTOR_LOG_FILE, level=logging.INFO ):
    """
    Configure the shared speed_test logger hierarchy.

    Child loggers use names such as:
      speed_test.collector
      speed_test.scheduler
      speed_test.database

    Console diagnostics are written to stderr so CLI stdout remains suitable
    for machine-readable JSON output.
    """

    root_logger = logging.getLogger( ROOT_LOGGER_NAME )

    if getattr( root_logger, "_speed_test_configured", False ):
        return root_logger

    LOG_DIR.mkdir( parents=True, exist_ok=True )

    root_logger.setLevel( level )
    root_logger.propagate = False

    formatter = logging.Formatter(
        "%(asctime)sZ | %(name)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S"
    )

    formatter.converter = time.gmtime

    console_handler = logging.StreamHandler( sys.stderr)
    console_handler.setLevel( level )
    console_handler.setFormatter( formatter )

    file_handler = logging.FileHandler( log_file, encoding="utf-8" )
    file_handler.setLevel( level )
    file_handler.setFormatter( formatter )

    root_logger.addHandler( console_handler )
    root_logger.addHandler( file_handler )

    root_logger._speed_test_configured = True

    return root_logger


# Get a logger for a specific component of the speed_test application.
def get_logger( component ):
    return logging.getLogger( f"{ROOT_LOGGER_NAME}.{component}" )
