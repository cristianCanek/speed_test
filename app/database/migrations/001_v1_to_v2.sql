BEGIN IMMEDIATE;

CREATE TABLE IF NOT EXISTS schema_version (
    version        INTEGER PRIMARY KEY,
    applied_at_utc TEXT    NOT NULL,
    description    TEXT    NOT NULL
);

CREATE TABLE IF NOT EXISTS speedtest_runs (
    id                                  INTEGER PRIMARY KEY AUTOINCREMENT,
    legacy_raw_result_id                INTEGER UNIQUE,

    status                              TEXT    NOT NULL
                                                CHECK( status IN ( 'success', 'failed', 'missing' ) ),

    timestamp_utc                       TEXT    NOT NULL,

    type                                TEXT,

    ping_jitter_ms                      REAL,
    ping_latency_ms                     REAL,
    ping_low_ms                         REAL,
    ping_high_ms                        REAL,

    download_bandwidth_bytes_per_second INTEGER,
    download_bytes                      INTEGER,
    download_elapsed_ms                 INTEGER,
    download_latency_iqm_ms             REAL,
    download_latency_low_ms             REAL,
    download_latency_high_ms            REAL,
    download_latency_jitter_ms          REAL,

    upload_bandwidth_bytes_per_second   INTEGER,
    upload_bytes                        INTEGER,
    upload_elapsed_ms                   INTEGER,
    upload_latency_iqm_ms               REAL,
    upload_latency_low_ms               REAL,
    upload_latency_high_ms              REAL,
    upload_latency_jitter_ms            REAL,

    isp                                 TEXT,

    interface_internal_ip               TEXT,
    interface_name                      TEXT,
    interface_mac_address               TEXT,
    interface_is_vpn                    INTEGER CHECK( interface_is_vpn IN ( 0, 1 ) OR interface_is_vpn IS NULL ),
    interface_external_ip               TEXT,

    server_id                           INTEGER,
    server_host                         TEXT,
    server_port                         INTEGER,
    server_name                         TEXT,
    server_location                     TEXT,
    server_country                      TEXT,
    server_ip                           TEXT,

    result_id                           TEXT,
    result_url                          TEXT,
    result_persisted                    INTEGER CHECK( result_persisted IN ( 0, 1 ) OR result_persisted IS NULL ),

    error_type                          TEXT,
    error_message                       TEXT,
    exit_code                           INTEGER,

    created_at_utc                      TEXT    NOT NULL
                                                DEFAULT ( strftime( '%Y-%m-%dT%H:%M:%fZ', 'now' ) )
);

INSERT INTO speedtest_runs (
    legacy_raw_result_id,
    status,
    timestamp_utc,
    type,
    ping_jitter_ms,
    ping_latency_ms,
    ping_low_ms,
    ping_high_ms,
    download_bandwidth_bytes_per_second,
    download_bytes,
    download_elapsed_ms,
    download_latency_iqm_ms,
    download_latency_low_ms,
    download_latency_high_ms,
    download_latency_jitter_ms,
    upload_bandwidth_bytes_per_second,
    upload_bytes,
    upload_elapsed_ms,
    upload_latency_iqm_ms,
    upload_latency_low_ms,
    upload_latency_high_ms,
    upload_latency_jitter_ms,
    isp,
    interface_internal_ip,
    interface_name,
    interface_mac_address,
    interface_is_vpn,
    interface_external_ip,
    server_id,
    server_host,
    server_port,
    server_name,
    server_location,
    server_country,
    server_ip,
    result_id,
    result_url,
    result_persisted
)
SELECT
    rawResult_id,
    'success',
    strftime( '%Y-%m-%dT%H:%M:%fZ', timestamp ),
    type,
    ping_jitter,
    ping_latency,
    ping_low,
    ping_high,
    download_bandwith,
    download_bytes,
    download_elapsed,
    download_latency_iqm,
    download_latency_low,
    download_latency_high,
    download_latency_jitter,
    upload_bandwith,
    upload_bytes,
    upload_elapsed,
    upload_latency_iqm,
    upload_latency_low,
    upload_latency_high,
    upload_latency_jitter,
    isp,
    interface_internalIp,
    interface_name,
    interface_macAddr,
    interface_isVpn,
    interface_externalIp,
    server_id,
    server_host,
    server_port,
    server_name,
    server_location,
    server_country,
    server_ip,
    result_id,
    result_url,
    result_persisted
FROM rawResults
ORDER BY rawResult_id ASC;

CREATE INDEX IF NOT EXISTS idx_speedtest_runs_timestamp
    ON speedtest_runs ( timestamp_utc ASC );

CREATE INDEX IF NOT EXISTS idx_speedtest_runs_status_timestamp
    ON speedtest_runs ( status, timestamp_utc ASC );

CREATE INDEX IF NOT EXISTS idx_speedtest_runs_result_id
    ON speedtest_runs ( result_id );

INSERT OR IGNORE INTO schema_version (
    version,
    applied_at_utc,
    description
)
VALUES (
    1,
    strftime( '%Y-%m-%dT%H:%M:%fZ', 'now' ),
    'Legacy Version 1 schema detected'
);

INSERT OR REPLACE INTO schema_version (
    version,
    applied_at_utc,
    description
)
VALUES (
    2,
    strftime( '%Y-%m-%dT%H:%M:%fZ', 'now' ),
    'Migrated Version 1 historical data to Version 2 schema'
);

COMMIT;
