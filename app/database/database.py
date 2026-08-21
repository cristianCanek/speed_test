#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import sqlite3

from pathlib import Path


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

DATABASE_FILE = Path( "/config/data/speedtest.sqlite3" )
SCHEMA_FILE   = Path( "/app/database/schema.sql"       )


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Create a Version 1-compatible SQLite database only when one does not already exist.
def ensure_database():
    if DATABASE_FILE.exists():
        return

    DATABASE_FILE.parent.mkdir( parents=True, exist_ok=True )

    schema = SCHEMA_FILE.read_text( encoding="utf-8" )
    conn = None

    try:
        conn = sqlite3.connect( DATABASE_FILE )
        conn.executescript( schema )
        conn.commit()
        print( f"Database created at {DATABASE_FILE}." )
    except Exception:
        if conn is not None:
            conn.close()
            conn = None

        # Do not leave a partially initialized database behind.
        DATABASE_FILE.unlink( missing_ok=True )
        raise
    finally:
        if conn is not None:
            conn.close()
