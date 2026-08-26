#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import subprocess

from dataclasses import dataclass
from pathlib     import Path


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

SPEEDTEST_BINARY        = Path( "/app/bin/speedtest" )
DEFAULT_TIMEOUT_SECONDS = 120


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

# Represents the result of executing the Ookla Speedtest CLI.
@dataclass
class CliExecution:
    stdout: str
    stderr: str
    exit_code: int | None
    timed_out: bool = False


# Represents the Ookla Speedtest CLI command-line interface.
class OoklaCli:
    def __init__( self, executable=SPEEDTEST_BINARY,  timeout_seconds=DEFAULT_TIMEOUT_SECONDS ):
        self.executable      = Path( executable )
        self.timeout_seconds = timeout_seconds

    def run( self ):
        command = [
            str( self.executable ),
            "--accept-license",
            "--accept-gdpr",
            "-f",
            "json-pretty"
        ]

        try:
            completed = subprocess.run(
                command,
                capture_output = True,
                text           = True,
                timeout        = self.timeout_seconds,
                check          = False
            )

            return CliExecution(
                stdout    = completed.stdout,
                stderr    = completed.stderr,
                exit_code = completed.returncode
            )

        except subprocess.TimeoutExpired as err:
            stdout = err.stdout or ""
            stderr = err.stderr or ""

            if isinstance( stdout, bytes ):
                stdout = stdout.decode( errors="replace" )

            if isinstance( stderr, bytes ):
                stderr = stderr.decode( errors="replace" )

            return CliExecution(
                stdout    = stdout,
                stderr    = stderr,
                exit_code = None,
                timed_out = True
            )

        except FileNotFoundError:
            return CliExecution(
                stdout    = "",
                stderr    = f"Ookla Speedtest CLI not found at '{self.executable}'.",
                exit_code = None
            )
