#!/usr/bin/env python

# ======================================================================================================================
# Imports.
# ======================================================================================================================

from dataclasses import asdict, dataclass
from enum import StrEnum
from typing import Any


# ======================================================================================================================
# Classes definition.
# ======================================================================================================================

# Represents the execution status of the collector.
class ExecutionStatus( StrEnum ):
    SUCCESS = "success"
    FAILED  = "failed"
    MISSING = "missing"


# Represents a single Ookla Speedtest measurement.
@dataclass
class SpeedtestMeasurement:
    timestamp_utc : str
    type          : str

    ping_jitter_ms  : float
    ping_latency_ms : float
    ping_low_ms     : float
    ping_high_ms    : float

    download_bandwidth_bytes_per_second : int
    download_bytes                      : int
    download_elapsed_ms                 : int
    download_latency_iqm_ms             : float
    download_latency_low_ms             : float
    download_latency_high_ms            : float
    download_latency_jitter_ms          : float

    upload_bandwidth_bytes_per_second : int
    upload_bytes                      : int
    upload_elapsed_ms                 : int
    upload_latency_iqm_ms             : float
    upload_latency_low_ms             : float
    upload_latency_high_ms            : float
    upload_latency_jitter_ms          : float

    isp: str

    interface_internal_ip : str
    interface_name        : str
    interface_mac_address : str
    interface_is_vpn      : bool
    interface_external_ip : str

    server_id       : int
    server_host     : str
    server_port     : int
    server_name     : str
    server_location : str
    server_country  : str
    server_ip       : str

    result_id        : str
    result_url       : str
    result_persisted : bool

    def to_public_dict( self ):
        return {
            "timestamp"        : self.timestamp_utc,
            "download_mbps"    : round( self.download_bandwidth_bytes_per_second / 1_000_000 * 8, 2 ),
            "upload_mbps"      : round( self.upload_bandwidth_bytes_per_second   / 1_000_000 * 8, 2 ),
            "ping_ms"          : self.ping_latency_ms,
            "download_latency" : self.download_latency_iqm_ms,
            "upload_latency"   : self.upload_latency_iqm_ms,
            "result_url"       : self.result_url
        }


# Represents the outcome of executing a Speedtest measurement.
@dataclass
class CollectorOutcome:
    status        : ExecutionStatus
    persisted     : bool
    measurement   : SpeedtestMeasurement | None = None
    error_type    : str | None = None
    error_message : str | None = None
    exit_code     : int | None = None
    raw_output    : str | None = None

    def to_dict( self, include_raw=False ):
        payload: dict[str, Any] = {
            "status"        : self.status.value,
            "persisted"     : self.persisted,
            "error_type"    : self.error_type,
            "error_message" : self.error_message,
            "exit_code"     : self.exit_code,
            "result"        : (
                self.measurement.to_public_dict()
                if self.measurement is not None
                else None
            )
        }

        if include_raw:
            payload["raw_output"] = self.raw_output

        return payload
