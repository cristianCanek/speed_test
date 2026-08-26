#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

import json

from datetime import datetime, timezone

from collector.models import SpeedtestMeasurement


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

# Represents an error that occurred while parsing the Ookla Speedtest CLI output.
class SpeedtestParseError( ValueError ):
    def __init__( self, error_type, message ):
        super().__init__( message )
        self.error_type = error_type


# ======================================================================================================================
# Functions definition.
# ======================================================================================================================

# Normalizes a UTC timestamp string to ISO 8601 format with milliseconds precision and 'Z' suffix.
def _normalize_utc_timestamp( timestamp ):
    try:
        parsed = datetime.fromisoformat( timestamp.replace( "Z", "+00:00" ) )
    except ( AttributeError, ValueError ) as err:
        raise SpeedtestParseError( "malformed_output", f"Invalid Speedtest timestamp: {timestamp!r}." ) from err

    if parsed.tzinfo is None:
        raise SpeedtestParseError( "malformed_output", "Speedtest timestamp does not contain timezone information." )

    return (
        parsed.astimezone( timezone.utc )
        .isoformat( timespec="milliseconds" )
        .replace( "+00:00", "Z" )
    )


# Retrieves a required value from a nested dictionary, raising a SpeedtestParseError if the value is missing or null.
def _required( data, *path ):
    value = data

    try:
        for key in path:
            value = value[key]
    except ( KeyError, TypeError ) as err:
        dotted = ".".join( path )
        raise SpeedtestParseError( "malformed_output", f"Required Ookla JSON field '{dotted}' is missing." ) from err

    if value is None:
        dotted = ".".join( path )
        raise SpeedtestParseError( "malformed_output", f"Required Ookla JSON field '{dotted}' is null." )

    return value


# Parses the output of the Ookla Speedtest CLI and returns a SpeedtestMeasurement object.
def parse_speedtest_output( output ):
    if output is None or not output.strip():
        raise SpeedtestParseError( "empty_output", "Ookla Speedtest CLI returned an empty stdout payload." )

    try:
        data = json.loads( output )
    except json.JSONDecodeError as err:
        raise SpeedtestParseError( "invalid_json", f"Ookla Speedtest CLI returned invalid JSON: {err}." ) from err

    if not isinstance( data, dict ):
        raise SpeedtestParseError( "malformed_output", "Ookla Speedtest JSON root must be an object." )

    if _required( data, "type" ) != "result":
        raise SpeedtestParseError( "malformed_output", f"Unexpected Ookla payload type: {data.get('type')!r}." )

    return SpeedtestMeasurement(
        timestamp_utc = _normalize_utc_timestamp( _required( data, "timestamp" ) ),
        type          = str( _required( data, "type" ) ),

        ping_jitter_ms  = float( _required( data, "ping", "jitter"  ) ),
        ping_latency_ms = float( _required( data, "ping", "latency" ) ),
        ping_low_ms     = float( _required( data, "ping", "low"     ) ),
        ping_high_ms    = float( _required( data, "ping", "high"    ) ),

        download_bandwidth_bytes_per_second = int(   _required( data, "download", "bandwidth"         ) ),
        download_bytes                      = int(   _required( data, "download", "bytes"             ) ),
        download_elapsed_ms                 = int(   _required( data, "download", "elapsed"           ) ),
        download_latency_iqm_ms             = float( _required( data, "download", "latency", "iqm"    ) ),
        download_latency_low_ms             = float( _required( data, "download", "latency", "low"    ) ),
        download_latency_high_ms            = float( _required( data, "download", "latency", "high"   ) ),
        download_latency_jitter_ms          = float( _required( data, "download", "latency", "jitter" ) ),

        upload_bandwidth_bytes_per_second = int(   _required( data, "upload", "bandwidth"         ) ),
        upload_bytes                      = int(   _required( data, "upload", "bytes"             ) ),
        upload_elapsed_ms                 = int(   _required( data, "upload", "elapsed"           ) ),
        upload_latency_iqm_ms             = float( _required( data, "upload", "latency", "iqm"    ) ),
        upload_latency_low_ms             = float( _required( data, "upload", "latency", "low"    ) ),
        upload_latency_high_ms            = float( _required( data, "upload", "latency", "high"   ) ),
        upload_latency_jitter_ms          = float( _required( data, "upload", "latency", "jitter" ) ),

        isp = str( _required( data, "isp" ) ),

        interface_internal_ip = str(  _required( data, "interface", "internalIp" ) ),
        interface_name        = str(  _required( data, "interface", "name"       ) ),
        interface_mac_address = str(  _required( data, "interface", "macAddr"    ) ),
        interface_is_vpn      = bool( _required( data, "interface", "isVpn"      ) ),
        interface_external_ip = str(  _required( data, "interface", "externalIp" ) ),

        server_id       = int( _required( data, "server", "id"       ) ),
        server_host     = str( _required( data, "server", "host"     ) ),
        server_port     = int( _required( data, "server", "port"     ) ),
        server_name     = str( _required( data, "server", "name"     ) ),
        server_location = str( _required( data, "server", "location" ) ),
        server_country  = str( _required( data, "server", "country"  ) ),
        server_ip       = str( _required( data, "server", "ip"       ) ),

        result_id        = str(  _required( data, "result", "id"        ) ),
        result_url       = str(  _required( data, "result", "url"       ) ),
        result_persisted = bool( _required( data, "result", "persisted" ) )
    )
