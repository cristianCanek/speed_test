#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import re

from datetime import datetime, timedelta, timezone


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

RANGE_PATTERN = re.compile( r"^([1-9][0-9]*)([hd])$" )

MAX_HOURS = 24 * 365
MAX_DAYS  = 365


# ======================================================================================================================
# Exceptions.
# ======================================================================================================================

class RangeError( ValueError ):
    """Raised when an API dataset range is invalid."""


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Parse an API range.
def parse_range( value: str ):
    """
    Parse an API range.

    Supported examples:
      1h
      24h
      7d
      30d
      365d
      all
    """

    if value == "all":
        return None

    match = RANGE_PATTERN.fullmatch( value )

    if match is None:
        raise RangeError(
            "Range must use the format '<number>h', '<number>d', or 'all'."
        )

    amount = int( match.group( 1 ) )
    unit   = match.group( 2 )

    if unit == "h":
        if amount > MAX_HOURS:
            raise RangeError( f"Hour ranges cannot exceed {MAX_HOURS}h." )

        delta = timedelta( hours=amount )

    else:
        if amount > MAX_DAYS:
            raise RangeError( f"Day ranges cannot exceed {MAX_DAYS}d." )

        delta = timedelta( days=amount )

    threshold = datetime.now( timezone.utc ) - delta

    return threshold.isoformat().replace( "+00:00", "Z" )
