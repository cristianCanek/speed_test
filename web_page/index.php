<?php
    /* Data for accesing Database. */
    $db_hostname      = "my-own-domain.com";
    $db_name          = "my-database-name";
    $db_username      = "my-database-user";
    $db_user_password = "my-user's-password";

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

    $string_data = "[ ";

    /* Getting connected to the database. */
    $connection = mysqli_connect( $db_hostname, $db_username, $db_user_password, $db_name );

    /* Verifying we are connected to the database. */
    if ( mysqli_connect_errno() ) {
        printf( "Error: Connection error: %s\n", mysqli_connect_error() );
        exit();
    }

    /* Asking database for data. */
    if( $result = mysqli_query( $connection, "SELECT * FROM ST_RESULT ORDER BY timestamp" ) ) {
        while( $row = mysqli_fetch_assoc( $result ) ) {
            $data_st_result_id[]         = $row['st_result_id'];
            $data_type[]                 = $row['type'];
            $data_timestamp[]            = $row['timestamp'];
            $data_ping_jitter[]          = $row['ping_jitter'];
            $data_ping_latency[]         = $row['ping_latency'];
            $data_download_bandwith[]    = $row['download_bandwith'] / 1000 / 1000 * 8;
            $data_download_bytes[]       = $row['download_bytes'];
            $data_download_elapsed[]     = $row['download_elapsed'];
            $data_upload_bandwith[]      = $row['upload_bandwith'] / 1000 / 1000 * 8;
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
        }

        /* Free result data. */
        mysqli_free_result( $result );
    }

    /* Close database connection. */
    mysqli_close( $connection );

    $i = 0;

    while( $i < count( $data_timestamp ) - 1 ) {
        $string_data .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round( (float) $data_download_bandwith[$i], 2 )  . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "], ";
        $i++;
    }

    $string_data .= "[ new Date( " . (int) substr( $data_timestamp[$i], 0, 4 ) . ", " . ( (int) substr( $data_timestamp[$i], 5, 2 ) - 1 ) . ", " . (int) substr( $data_timestamp[$i], 8, 2 ) . ", " . (int) substr( $data_timestamp[$i], 11, 2 ) . ", " . (int) substr( $data_timestamp[$i], 14, 2 ) . " ), " . round ( (float) $data_download_bandwith[$i], 2 ) . " , " . round( (float) $data_upload_bandwith[$i], 2 ) . "] ]";
?>

<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
<script type="text/javascript">
    google.charts.load( 'current', { packages: [ 'corechart', 'line' ] } );
    google.charts.setOnLoadCallback( drawLinesChart );

    /* Draws the graph. */
    function drawLinesChart() {
        var data = new google.visualization.DataTable();

        data.addColumn( 'datetime', 'Date'        );
        data.addColumn( 'number', 'Download' );
        data.addColumn( 'number', 'Upload'   );

        data.addRows( <?php echo $string_data; ?> );

        var options = {
            hAxis: {
                title: 'Datetime',
                format: 'd/M/yy'
            },
            vAxis: {
                title: 'Conexion speed (Mbps)'
            },
            series: {
                1: { curveType: 'none' }
            }
        };

        var chart = new google.visualization.LineChart(document.getElementById('chart_div'));
        chart.draw(data, options);
    }
</script>

<div id="chart_div"></div>
