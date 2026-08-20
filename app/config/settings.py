#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import yaml

from pathlib  import Path
from shutil   import copyfile
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


# ======================================================================================================================
# Global declarations.
# ======================================================================================================================

CONFIG_DIR            = Path( "/config" )
DATA_DIR              = CONFIG_DIR / "data"
LOGS_DIR              = CONFIG_DIR / "logs"
SETTINGS_FILE         = CONFIG_DIR / "settings.yaml"
DEFAULT_SETTINGS_FILE = Path( "/app/config/settings.default.yaml" )

VALID_INTERVALS = ( 1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60 )


# ======================================================================================================================
# Exceptions.
# ======================================================================================================================

class SettingsError( Exception ):
    """Raised when the application settings are missing or invalid."""


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Create the persistent directory structure used by the application.
def ensure_config_structure():
    CONFIG_DIR.mkdir( parents=True, exist_ok=True )
    DATA_DIR.mkdir(   parents=True, exist_ok=True )
    LOGS_DIR.mkdir(   parents=True, exist_ok=True )


# Create the default settings file only when the user does not already have one.
def ensure_settings_file():
    if not SETTINGS_FILE.exists():
        try:
            copyfile( DEFAULT_SETTINGS_FILE, SETTINGS_FILE )
        except OSError as err:
            raise SettingsError(
                f"Unable to create default settings file at '{SETTINGS_FILE}': {err}"
            ) from None

        print( f"Default settings created at {SETTINGS_FILE}." )


# Validate the scheduler configuration.
def validate_settings( settings ):
    if not isinstance( settings, dict ):
        raise SettingsError("Settings file must contain a YAML mapping.")

    scheduler = settings.get( "scheduler" )

    if not isinstance( scheduler, dict ):
        raise SettingsError("Missing or invalid 'scheduler' settings section.")

    interval_minutes = scheduler.get( "interval_minutes" )
    timezone         = scheduler.get( "timezone" )

    if type( interval_minutes ) is not int:
        raise SettingsError( "'scheduler.interval_minutes' must be an integer." )

    if interval_minutes not in VALID_INTERVALS:
            valid_values = ", ".join( str( value ) for value in VALID_INTERVALS )
    
            raise SettingsError(
                f"'scheduler.interval_minutes' is set to {interval_minutes}. "
                "The value must be a positive divisor of 60 so executions remain "
                f"aligned to the clock. Valid values: {valid_values}."
            )

    if not isinstance( timezone, str ) or timezone.strip() == "":
        raise SettingsError( "'scheduler.timezone' must be a non-empty IANA timezone name." )
    
    try:
        ZoneInfo( timezone )
    except ZoneInfoNotFoundError:
        raise SettingsError(
            f"Unknown timezone '{timezone}'. Use a valid IANA timezone name, "
            "for example 'UTC' or 'America/Mexico_City'."
        ) from None


# Load and validate the persistent application settings.
def load_settings():
    ensure_config_structure()
    ensure_settings_file()

    try:
        with SETTINGS_FILE.open( "r", encoding="utf-8" ) as settings_file:
            settings = yaml.safe_load( settings_file )
    
    except yaml.YAMLError as err:
        raise SettingsError( f"Unable to parse '{SETTINGS_FILE}': {err}" ) from None
    
    except OSError as err:
        raise SettingsError( f"Unable to read '{SETTINGS_FILE}': {err}" ) from None

    validate_settings( settings )

    return settings
