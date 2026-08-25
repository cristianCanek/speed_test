#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import sqlite3

from pathlib import Path


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

DATABASE_FILE  = Path( "/config/data/speedtest.sqlite3" )
SCHEMA_FILE    = Path( "/app/database/schema.sql"       )
MIGRATIONS_DIR = Path( "/app/database/migrations"       )

CURRENT_SCHEMA_VERSION = 2


# ======================================================================================================================
# Exceptions.
# ======================================================================================================================

class DatabaseMigrationError( RuntimeError ):
    """Raised when the database schema cannot be created or migrated safely."""


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Check whether a SQLite table exists.
def _table_exists( conn, table_name ):
    row = conn.execute(
        """
        SELECT 1
        FROM   sqlite_master
        WHERE  type = 'table'
        AND    name = ?
        LIMIT  1
        """,
        ( table_name, )
    ).fetchone()

    return row is not None


# Get the currently installed schema version.
def get_schema_version( conn ):
    if _table_exists( conn, "schema_version" ):
        row = conn.execute( "SELECT MAX( version ) FROM schema_version" ).fetchone()

        if row is None or row[0] is None:
            raise DatabaseMigrationError(
                "The schema_version table exists but does not contain a schema version."
            )

        return int( row[0] )

    # Version 1 did not include schema_version. Detect it by its legacy table.
    if _table_exists( conn, "rawResults" ):
        return 1

    return 0


# Create a fresh Version 2 database.
def _create_database():
    DATABASE_FILE.parent.mkdir( parents=True, exist_ok=True )

    schema = SCHEMA_FILE.read_text( encoding="utf-8" )
    conn   = None

    try:
        conn = sqlite3.connect( DATABASE_FILE )
        conn.executescript( schema )
        conn.commit()

        print(
            f"Database created at {DATABASE_FILE} "
            f"with schema version {CURRENT_SCHEMA_VERSION}."
        )

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


# Apply one migration to an existing database.
def _apply_migration( conn, from_version ):
    if from_version == 1:
        migration_file = MIGRATIONS_DIR / "001_v1_to_v2.sql"
    else:
        raise DatabaseMigrationError(
            f"No migration path is defined from schema version {from_version}."
        )

    migration = migration_file.read_text( encoding="utf-8" )

    try:
        conn.executescript( migration )

    except sqlite3.Error as err:
        # The migration script contains its own transaction. Roll back here as
        # a safety net if SQLite still has an open transaction.
        if conn.in_transaction:
            conn.rollback()

        raise DatabaseMigrationError(
            f"Database migration from version {from_version} failed: {err}"
        ) from None


# Create or migrate the persistent SQLite database.
def ensure_database():
    if not DATABASE_FILE.exists():
        _create_database()
        return

    conn = sqlite3.connect( DATABASE_FILE )

    try:
        version = get_schema_version( conn )

        if version == 0:
            raise DatabaseMigrationError(
                "Existing SQLite database does not match a supported speed_test schema."
            )

        if version > CURRENT_SCHEMA_VERSION:
            raise DatabaseMigrationError(
                f"Database schema version {version} is newer than the supported "
                f"version {CURRENT_SCHEMA_VERSION}."
            )

        while version < CURRENT_SCHEMA_VERSION:
            print(
                f"Migrating database schema from version {version} "
                f"to version {version + 1}."
            )

            _apply_migration( conn, version )
            version = get_schema_version( conn )

        print( f"Database schema version: {version}." )

    finally:
        conn.close()
