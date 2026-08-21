CREATE TABLE rawResults (
    rawResult_id            INTEGER PRIMARY KEY AUTOINCREMENT,
    type                    TEXT ( 16 ),
    timestamp               INTEGER,
    ping_jitter             REAL,
    ping_latency            REAL,
    ping_low                REAL,
    ping_high               REAL,
    download_bandwith       INTEGER,
    download_bytes          INTEGER,
    download_elapsed        INTEGER,
    download_latency_iqm    REAL,
    download_latency_low    REAL,
    download_latency_high   REAL,
    download_latency_jitter REAL,
    upload_bandwith         INTEGER,
    upload_bytes            INTEGER,
    upload_elapsed          INTEGER,
    upload_latency_iqm      REAL,
    upload_latency_low      REAL,
    upload_latency_high     REAL,
    upload_latency_jitter   REAL,
    isp                     TEXT ( 64 ),
    interface_internalIp    TEXT ( 16 ),
    interface_name          TEXT ( 16 ),
    interface_macAddr       TEXT ( 18 ),
    interface_isVpn         INTEGER ( 1 ),
    interface_externalIp    TEXT ( 16 ),
    server_id               INTEGER,
    server_host             TEXT ( 64 ),
    server_port             INTEGER,
    server_name             TEXT ( 32 ),
    server_location         TEXT ( 64 ),
    server_country          TEXT ( 32 ),
    server_ip               TEXT ( 16 ),
    result_id               TEXT ( 36 ),
    result_url              TEXT ( 72 ),
    result_persisted        INTEGER ( 1 )
);

CREATE INDEX idx_rawResults_timestamp ON rawResults ( timestamp ASC );

CREATE VIEW rawResults_day AS
    SELECT   *
    FROM     rawResults
    WHERE    datetime( timestamp ) > datetime( 'now', '-1.0 days' )
    ORDER BY timestamp ASC;

CREATE VIEW rawResults_last AS
    SELECT *
    FROM   rawResults
    WHERE  timestamp = ( SELECT max( timestamp ) FROM rawResults );

CREATE VIEW rawResults_month AS
    SELECT   *
    FROM     rawResults
    WHERE    datetime( timestamp ) > datetime( 'now', '-1.0 months' )
    ORDER BY timestamp ASC;

CREATE VIEW rawResults_week AS
    SELECT   *
    FROM     rawResults
    WHERE    datetime( timestamp ) > datetime( 'now', '-7.0 days' )
    ORDER BY timestamp ASC;
