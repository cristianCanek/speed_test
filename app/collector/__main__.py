#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from collector.command import main as command_main


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# The collector module now exposes only manual execution commands.
#
# Scheduled execution is owned by the FastAPI application lifecycle in Alpha 8,
# which prevents accidentally starting a second scheduler inside the container.
def main():
    raise SystemExit(
        command_main()
    )


# ======================================================================================================================
# Main program.
# ======================================================================================================================

if __name__ == "__main__":
    main()
