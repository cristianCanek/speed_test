<?php

// =============================================================================
// Global declarations.
// =============================================================================

// ---- CONSTANTS --------------------------------------------------------------

// Database's name.
const DB_NAME = "/config/data/speedtest.sqlite3";


// =============================================================================
// Classes definition.
// =============================================================================

class MyDB extends SQLite3 {
    function __construct() {
        $this->open( DB_NAME, SQLITE3_OPEN_READONLY );
    }
}


// =============================================================================
// Functions definition.
// =============================================================================

// Convert one SQLite result set into the compact array format consumed by
// Chart.js:
//
// [
//     [ timestamp, download, upload, ping, download_latency, upload_latency ],
//     ...
// ]
function resultToChartData( $result ) {
    $data = [];

    while ( $row = $result->fetchArray( SQLITE3_ASSOC ) ) {
        $data[] = [
            $row['timestamp'],
            (float) $row['download_bandwith'],
            (float) $row['upload_bandwith'],
            (int)   $row['ping_latency'],
            (int)   $row['download_latency_iqm'],
            (int)   $row['upload_latency_iqm']
        ];
    }

    return $data;
}


// =============================================================================
// Main program.
// =============================================================================

$conn = new MyDB();

$bootstrap_data = [
    "last" => null,
    "ranges" => [
        "day"   => [],
        "week"  => [],
        "month" => []
    ]
];


// Get last result data.
$result_last = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith   as float ) / 1000 / 1000 * 8, 2 ) as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as   INT )                              as upload_latency_iqm,
            result_url
     FROM rawResults_last"
);

if ( $row = $result_last->fetchArray( SQLITE3_ASSOC ) ) {
    $bootstrap_data["last"] = [
        "timestamp"        => $row['timestamp'],
        "download_mbps"    => (float) $row['download_bandwith'],
        "upload_mbps"      => (float) $row['upload_bandwith'],
        "ping_ms"          => (int)   $row['ping_latency'],
        "download_latency" => (int)   $row['download_latency_iqm'],
        "upload_latency"   => (int)   $row['upload_latency_iqm'],
        "result_url"       => $row['result_url']
    ];
}

// Get last 1 day's data.
$result_day = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith   as float ) / 1000 / 1000 * 8, 2 ) as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as   INT )                              as upload_latency_iqm
     FROM rawResults_day
     ORDER BY timestamp ASC"
);

$bootstrap_data["ranges"]["day"] = resultToChartData( $result_day );

// Get last 7 days data.
$result_week = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith   as float ) / 1000 / 1000 * 8, 2 ) as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as   INT )                              as upload_latency_iqm
     FROM rawResults_week
     ORDER BY timestamp ASC"
);

$bootstrap_data["ranges"]["week"] = resultToChartData( $result_week );

// Get last 1 month's data.
$result_month = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith   as float ) / 1000 / 1000 * 8, 2 ) as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as   INT )                              as upload_latency_iqm
     FROM rawResults_month
     ORDER BY timestamp ASC"
);

$bootstrap_data["ranges"]["month"] = resultToChartData( $result_month );

// Encode the complete bootstrap payload once. PHP is now responsible only for
// data access; presentation is handled by HTML/CSS/JavaScript.
$bootstrap_data_json = json_encode(
    $bootstrap_data,
    JSON_UNESCAPED_SLASHES | JSON_HEX_TAG | JSON_HEX_AMP | JSON_HEX_APOS | JSON_HEX_QUOT
);

// Closing the database connection.
$conn->close();

?>
