<?php
    /* Data for accesing Database. */
    $db_hostname      = "my-own-domain.com";
    $db_name          = "my-database-name";
    $db_username      = "my-database-user";
    $db_user_password = "my-user's-password";

    $query_string = "SELECT st_result_id, "                                                                  .
                           "type, "                                                                          .
                           "timestamp, "                                                                     .
                           "ping_jitter, "                                                                   .
                           "ping_latency, "                                                                  .
                           "download_bandwith, "                                                             .
                           "download_bytes, "                                                                .
                           "download_elapsed, "                                                              .
                           "upload_bandwith, "                                                               .
                           "upload_bytes, "                                                                  .
                           "upload_elapsed, "                                                                .
                           "packetLoss, "                                                                    .
                           "isp, "                                                                           .
                           "interface_internalIp, "                                                          .
                           "interface_name, "                                                                .
                           "interface_macAddr, "                                                             .
                           "interface_isVpn, "                                                               .
                           "interface_externalIp, "                                                          .
                           "server_id, "                                                                     .
                           "server_name, "                                                                   .
                           "server_location, "                                                               .
                           "server_country, "                                                                .
                           "server_host, "                                                                   .
                           "server_port, "                                                                   .
                           "server_ip, "                                                                     .
                           "result_id, "                                                                     .
                           "result_url, "                                                                    .
                           "IF( timestamp > DATE_SUB( CURRENT_TIMESTAMP, INTERVAL 24 HOUR ), 1, 0 ) today, " .
                           "IF( timestamp > DATE_SUB( CURRENT_TIMESTAMP, INTERVAL  7 DAY  ), 1, 0 ) week, "  .
                           "IF( timestamp > DATE_SUB( CURRENT_TIMESTAMP, INTERVAL 30 DAY  ), 1, 0 ) month "  .
                    "FROM( SELECT st_result_id, "                                                            .
                                 "type, "                                                                    .
                                 "DATE_SUB( timestamp, INTERVAL 5 HOUR ) timestamp, "                        .
                                 "ping_jitter, "                                                             .
                                 "ping_latency, "                                                            .
                                 "download_bandwith / 1000 / 1000 * 8 download_bandwith, "                   .
                                 "download_bytes, "                                                          .
                                 "download_elapsed, "                                                        .
                                 "upload_bandwith / 1000 / 1000 * 8 upload_bandwith, "                       .
                                 "upload_bytes, "                                                            .
                                 "upload_elapsed, "                                                          .
                                 "packetLoss, "                                                              .
                                 "isp, "                                                                     .
                                 "interface_internalIp, "                                                    .
                                 "interface_name, "                                                          .
                                 "interface_macAddr, "                                                       .
                                 "interface_isVpn, "                                                         .
                                 "interface_externalIp, "                                                    .
                                 "server_id, "                                                               .
                                 "server_name, "                                                             .
                                 "server_location, "                                                         .
                                 "server_country, "                                                          .
                                 "server_host, "                                                             .
                                 "server_port, "                                                             .
                                 "result_id, "                                                               .
                                 "server_ip, "                                                               .
                                 "result_url "                                                               .
                          "FROM ST_RESULT "                                                                  .
                          "WHERE DATE_SUB( timestamp, INTERVAL 5 HOUR ) > DATE_SUB( CURRENT_DATE, INTERVAL 30 DAY ) " .
                          "ORDER BY timestamp) ALL_DATA "                                                    .
                    "ORDER BY timestamp";

    $data_st_result_id         = array();
    $data_type                 = array();
    $data_timestamp            = array();
    $data_ping_jitter          = array();
    $data_ping_latency         = array();
    $data_download_bandwith    = array();
    $data_download_bytes       = array();
    $data_download_elapsed     = array();
    $data_upload_bandwith      = array();
    $data_upload_bytes         = array();
    $data_upload_elapsed       = array();
    $data_packetLoss           = array();
    $data_isp                  = array();
    $data_interface_internalIp = array();
    $data_interface_name       = array();
    $data_interface_macAddr    = array();
    $data_interface_isVpn      = array();
    $data_interface_externalIp = array();
    $data_server_id            = array();
    $data_server_name          = array();
    $data_server_location      = array();
    $data_server_country       = array();
    $data_server_host          = array();
    $data_server_port          = array();
    $data_server_ip            = array();
    $data_result_id            = array();
    $data_result_url           = array();
    $data_result_today         = array();
    $data_result_week          = array();
    $data_result_month         = array();

    $string_data_today = "[ ";
    $string_data_week  = "[ ";
    $string_data_month = "[ ";

    /* Last speed test result. */
    $lst_download   = 0;
    $lst_upload     = 0;
    $lst_ping       = 0;
    $lst_result_url = "";
    $lst_timestamp  = "";

    /* Getting connected to the database. */
    $connection = mysqli_connect( $db_hostname, $db_username, $db_user_password, $db_name );

    /* Verifying we are connected to the database. */
    if ( mysqli_connect_errno() ) {
        printf( "Error: Connection error: %s\n", mysqli_connect_error() );
        exit();
    }

    /* Asking database for data. */
    if( $result = mysqli_query( $connection, $query_string ) ) {
        while( $row = mysqli_fetch_assoc( $result ) ) {
            $data_st_result_id[]         = $row['st_result_id'];
            $data_type[]                 = $row['type'];
            $data_timestamp[]            = $row['timestamp'];
            $data_ping_jitter[]          = $row['ping_jitter'];
            $data_ping_latency[]         = $row['ping_latency'];
            $data_download_bandwith[]    = $row['download_bandwith'];
            $data_download_bytes[]       = $row['download_bytes'];
            $data_download_elapsed[]     = $row['download_elapsed'];
            $data_upload_bandwith[]      = $row['upload_bandwith'];
            $data_upload_bytes[]         = $row['upload_bytes'];
            $data_upload_elapsed[]       = $row['upload_elapsed'];
            $data_packetLoss[]           = $row['packetLoss'];
            $data_isp[]                  = $row['isp'];
            $data_interface_internalIp[] = $row['interface_internalIp'];
            $data_interface_name[]       = $row['interface_name'];
            $data_interface_macAddr[]    = $row['interface_macAddr'];
            $data_interface_isVpn[]      = $row['interface_isVpn'];
            $data_interface_externalIp[] = $row['interface_externalIp'];
            $data_server_id[]            = $row['server_id'];
            $data_server_name[]          = $row['server_name'];
            $data_server_location[]      = $row['server_location'];
            $data_server_country[]       = $row['server_country'];
            $data_server_host[]          = $row['server_host'];
            $data_server_port[]          = $row['server_port'];
            $data_server_ip[]            = $row['server_ip'];
            $data_result_id[]            = $row['result_id'];
            $data_result_url[]           = $row['result_url'];
            $data_result_today[]         = $row['today'];
            $data_result_week[]          = $row['week'];
            $data_result_month[]         = $row['month'];
        }

        /* Free result data. */
        mysqli_free_result( $result );
    }

    /* Close database connection. */
    mysqli_close( $connection );

    $i = 0;

    while( $i < count( $data_st_result_id ) - 1 ) {
        $string_data_month .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 )  . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "], ";

        if( $data_result_week[$i] == '1' ) {
          $string_data_week .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 )  . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "], ";
        }

        if( $data_result_today[$i] == '1' ) {
          $string_data_today .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 )  . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "], ";
        }

        $i++;
    }

    /* Last data belongs to the current month, week and day by default. */
    $string_data_month .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 ) . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "] ]";
    $string_data_week  .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 ) . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "] ]";
    $string_data_today .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 ) . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "] ]";

    /* Last speed test result. */
    $lst_timestamp  = substr( $data_timestamp[$i], 0, -3 );
    $lst_download   = round( (float) $data_download_bandwith[$i], 2 );
    $lst_upload     = round( (float) $data_upload_bandwith[$i],   2 );
    $lst_ping       = round( (int)   $data_ping_latency[$i]         );
    $lst_result_url = $data_result_url[$i];
?>
