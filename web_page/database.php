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
// Strings with database data, used by the charts generator.
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
// Main program.
// =============================================================================

// set the default timezone to use.
date_default_timezone_set( 'America/Mexico_City' );

$conn = new MyDB();

// Get last result data.
$result_last = $conn->query( "SELECT timestamp, round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2) as download_bandwith, round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2) as upload_bandwith, CAST( ping_latency as INT ) as ping_latency, CAST( download_latency_iqm as INT ) as download_latency_iqm, CAST( upload_latency_iqm as INT ) as upload_latency_iqm, result_url FROM rawResults_last" );

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
$result_day = $conn->query( "SELECT timestamp, round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2) as download_bandwith, round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2) as upload_bandwith, CAST( ping_latency as INT ) as ping_latency, CAST( download_latency_iqm as INT ) as download_latency_iqm, CAST( upload_latency_iqm as INT ) as upload_latency_iqm FROM rawResults_day order by timestamp asc" );

$string_data_day = "[";

while ( $row = $result_day->fetchArray() ) {
    $string_data_day .= " [ new Date(\"" . $row['timestamp'] . "\"), " . $row['download_bandwith'] . " , " . $row['upload_bandwith'] . " , " . $row['ping_latency'] . " , " . $row['download_latency_iqm'] . " , " . $row['upload_latency_iqm'] . "],";
}

$string_data_day = substr( $string_data_day, 0, -1 ) . " ]";

// Get last 7 days data.
$result_week = $conn->query( "SELECT timestamp, round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2) as download_bandwith, round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2) as upload_bandwith, CAST( ping_latency as INT ) as ping_latency, CAST( download_latency_iqm as INT ) as download_latency_iqm, CAST( upload_latency_iqm as INT ) as upload_latency_iqm FROM rawResults_week order by timestamp asc" );

$string_data_week = "[";

while ( $row = $result_week->fetchArray() ) {
    $string_data_week .= " [ new Date(\"" . $row['timestamp'] . "\"), " . $row['download_bandwith'] . " , " . $row['upload_bandwith'] . " , " . $row['ping_latency'] . " , " . $row['download_latency_iqm'] . " , " . $row['upload_latency_iqm'] . "],";
}

$string_data_week = substr( $string_data_week, 0, -1 ) . " ]";

// Get last 1 month's data.
$result_month = $conn->query( "SELECT timestamp, round( CAST( download_bandwith as float ) / 1000 / 1000 * 8, 2) as download_bandwith, round( CAST( upload_bandwith as float ) / 1000 / 1000 * 8, 2) as upload_bandwith, CAST( ping_latency as INT ) as ping_latency, CAST( download_latency_iqm as INT ) as download_latency_iqm, CAST( upload_latency_iqm as INT ) as upload_latency_iqm FROM rawResults_month order by timestamp asc" );

$string_data_month = "[";

while ( $row = $result_month->fetchArray() ) {
    $string_data_month .= " [ new Date(\"" . $row['timestamp'] . "\"), " . $row['download_bandwith'] . " , " . $row['upload_bandwith'] . " , " . $row['ping_latency'] . " , " . $row['download_latency_iqm'] . " , " . $row['upload_latency_iqm'] . "],";
}

$string_data_month = substr( $string_data_month, 0, -1 ) . " ]";

// Closing the database connection.
$conn->close();

?>