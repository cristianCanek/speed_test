<?php

// =============================================================================
// Imports.
// =============================================================================


// =============================================================================
// Global declarations.
// =============================================================================

// ---- CONSTANTS --------------------------------------------------------------

// Database's name.
const DB_NAME = "/config/data/speedtest.sqlite3";

// ---- GLOBAL VARIABLES -------------------------------------------------------

// JSON strings with database data, used by Chart.js.
$string_data_day   = "[]";
$string_data_week  = "[]";
$string_data_month = "[]";

// Last speedtest results.
$last_timestamp            = 0;
$last_download_bandwith    = 0.0;
$last_upload_bandwith      = 0.0;
$last_ping_latency         = 0;
$last_download_latency_iqm = 0;
$last_upload_latency_iqm   = 0;
$last_result_url           = "";


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

    return json_encode( $data, JSON_UNESCAPED_SLASHES );
}


// =============================================================================
// Main program.
// =============================================================================

// Set the default timezone to use.
date_default_timezone_set( 'America/Mexico_City' );

$conn = new MyDB();

// Get last result data.
$result_last = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2 )   as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as INT )                                as upload_latency_iqm,
            result_url
     FROM rawResults_last"
);

while ( $row = $result_last->fetchArray() ) {
    $last_timestamp            = date( 'd/m/Y h:i A', strtotime( $row['timestamp'] ) );
    $last_download_bandwith    = $row['download_bandwith'];
    $last_upload_bandwith      = $row['upload_bandwith'];
    $last_ping_latency         = $row['ping_latency'];
    $last_download_latency_iqm = $row['download_latency_iqm'];
    $last_upload_latency_iqm   = $row['upload_latency_iqm'];
    $last_result_url           = $row['result_url'];
}

// Get last 1 day's data.
$result_day = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2 )   as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as INT )                                as upload_latency_iqm
     FROM rawResults_day
     ORDER BY timestamp ASC"
);

$string_data_day = resultToChartData( $result_day );

// Get last 7 days data.
$result_week = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2 )   as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as INT )                                as upload_latency_iqm
     FROM rawResults_week
     ORDER BY timestamp ASC"
);

$string_data_week = resultToChartData( $result_week );

// Get last 1 month's data.
$result_month = $conn->query(
    "SELECT timestamp,
            round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2 ) as download_bandwith,
            round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2 )   as upload_bandwith,
            CAST( ping_latency as INT )                                      as ping_latency,
            CAST( download_latency_iqm as INT )                              as download_latency_iqm,
            CAST( upload_latency_iqm as INT )                                as upload_latency_iqm
     FROM rawResults_month
     ORDER BY timestamp ASC"
);

$string_data_month = resultToChartData( $result_month );

// Closing the database connection.
$conn->close();

?>
