-- Table to store speed test results.

CREATE TABLE ST_RESULT(
    st_result_id SERIAL,
    type         VARCHAR(16),
    timestamp    TIMESTAMP,

    ping_jitter  FLOAT UNSIGNED,
    ping_latency FLOAT UNSIGNED,

    download_bandwith BIGINT UNSIGNED,
    download_bytes    BIGINT UNSIGNED,
    download_elapsed  BIGINT UNSIGNED,

    upload_bandwith BIGINT UNSIGNED,
    upload_bytes    BIGINT UNSIGNED,
    upload_elapsed  BIGINT UNSIGNED,

    packetLoss INT UNSIGNED,
    isp        VARCHAR(128),

    interface_internalIp VARCHAR(16),
    interface_name       VARCHAR(16),
    interface_macAddr    VARCHAR(32),
    interface_isVpn      VARCHAR(8),
    interface_externalIp VARCHAR(16),

    server_id       INT UNSIGNED,
    server_name     VARCHAR(32),
    server_location VARCHAR(32),
    server_country  VARCHAR(32),
    server_host     VARCHAR(32),
    server_port     INT UNSIGNED,
    server_ip       VARCHAR(16),

    result_id  VARCHAR(64),
    result_url VARCHAR(128),

    PRIMARY KEY(st_result_id)
);
