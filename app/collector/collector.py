#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import fcntl

from pathlib import Path

from collector.cli            import OoklaCli
from collector.models         import CollectorOutcome, ExecutionStatus
from collector.parser         import SpeedtestParseError, parse_speedtest_output
from collector.repository     import SpeedtestRepository
from logging_config           import configure_logging, get_logger


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

LOCK_FILE = Path( "/config/data/speedtest.lock" )


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

# Represents the Ookla Speedtest collector, which executes the Ookla Speedtest CLI and handles the results.
class SpeedtestCollector:
    def __init__( self,  cli=None, repository=None, logger=None ):
        configure_logging()
        
        self.cli        = cli or OoklaCli()
        self.repository = repository or SpeedtestRepository()
        self.logger     = logger or get_logger( "collector" )

    def execute( self, save=True, source="manual" ):

        LOCK_FILE.parent.mkdir( parents=True, exist_ok=True )

        # The lock file is intentionally persistent. flock() locks the open
        # file descriptor; the existence of this file does not mean the
        # collector is currently locked.
        with LOCK_FILE.open( "a" ) as lock_file:
            try:
                fcntl.flock( lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB )
            except BlockingIOError:
                message = ( "Speedtest execution skipped because another execution already holds the collector lock." )

                self.logger.warning( "%s execution skipped: overlap.", source )

                persisted = False

                if save:
                    self.repository.save_missing( "overlap", message )
                    persisted = True

                return CollectorOutcome(
                    status        = ExecutionStatus.MISSING,
                    persisted     = persisted,
                    error_type    = "overlap",
                    error_message = message
                )

            try:
                return self._execute_locked( save=save, source=source )
            finally:
                fcntl.flock( lock_file, fcntl.LOCK_UN )

    def _execute_locked( self, save, source ):
        self.logger.info( "%s Speedtest execution started.", source )

        execution = self.cli.run()

        if execution.timed_out:
            return self._failure(
                save          = save,
                source        = source,
                error_type    = "timeout",
                error_message = "Ookla Speedtest CLI execution timed out.",
                exit_code     = None,
                raw_output    = execution.stdout
            )

        if execution.exit_code is None:
            return self._failure(
                save          = save,
                source        = source,
                error_type    = "cli_not_found",
                error_message = ( execution.stderr.strip() or "Ookla Speedtest CLI could not be executed." ),
                exit_code     = None,
                raw_output    = execution.stdout
            )

        if execution.exit_code != 0:
            error_message = (
                execution.stderr.strip()
                or execution.stdout.strip()
                or f"Ookla Speedtest CLI exited with code {execution.exit_code}."
            )

            return self._failure(
                save          = save,
                source        = source,
                error_type    = "speedtest_cli_error",
                error_message = error_message,
                exit_code     = execution.exit_code,
                raw_output    = execution.stdout
            )

        try:
            measurement = parse_speedtest_output( execution.stdout )
        except SpeedtestParseError as err:
            return self._failure(
                save          = save,
                source        = source,
                error_type    = err.error_type,
                error_message = str( err ),
                exit_code     = execution.exit_code,
                raw_output    = execution.stdout
            )

        persisted = False

        if save:
            self.repository.save_success( measurement )
            persisted = True

        self.logger.info( "%s Speedtest execution succeeded%s.", source, " and was persisted" if persisted else "" )

        return CollectorOutcome(
            status      = ExecutionStatus.SUCCESS,
            persisted   = persisted,
            measurement = measurement,
            exit_code   = execution.exit_code,
            raw_output  = execution.stdout
        )

    def _failure( self, save, source, error_type, error_message, exit_code, raw_output ):
        persisted = False

        if save:
            self.repository.save_failed( error_type, error_message, exit_code )
            persisted = True

        self.logger.error( "%s Speedtest execution failed: %s: %s", source, error_type, error_message )

        return CollectorOutcome(
            status        = ExecutionStatus.FAILED,
            persisted     = persisted,
            error_type    = error_type,
            error_message = error_message,
            exit_code     = exit_code,
            raw_output    = raw_output
        )
