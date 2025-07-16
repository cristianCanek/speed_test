<?php require "database.php"; ?>

<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load( 'current', { packages: [ 'corechart', 'line' ] } );
            
            google.charts.setOnLoadCallback( drawLinesChart_Day   );
            google.charts.setOnLoadCallback( drawLinesChart_Week  );
            google.charts.setOnLoadCallback( drawLinesChart_Month );

            /* Draws the graph for Day's view. */
            function drawLinesChart_Day() {
                // Chart object.
                var chart = new google.visualization.LineChart( document.getElementById( 'chart_div_day' ) );

                // Data to be used for the chart.
                var data = new google.visualization.DataTable();

                // Format date values for x-axis.
                var formatter_shortdate = new google.visualization.DateFormat( { pattern: "dd/MM/yyyy KK:mm aa" } );

                // Chart settings.
                var options = {
                    title: 'SPEEDTEST Results (last 24 hrs)',
                    titleTextStyle: { color: '#FFFFFF', fontSize: 18 },
                    chartArea: { backgroundColor: '#1A1B2E', left: 70, width: 580 },
                    backgroundColor: '#141526',
                    width:  720,
                    height: 360,
                    legend: { textStyle: { color: '#9193A8', fontSize: 11 }, position: 'top' },
                    focusTarget: 'category',
                    tooltip: { textStyle: { fontSize: 11 } },
                    series: {
                        0: { targetAxisIndex: 0, color: '6AFFF3' },
                        1: { targetAxisIndex: 0, color: 'BF71FF' },
                        2: { targetAxisIndex: 1, color: 'FFF38E', lineDashStyle: [2, 2], lineWidth: 1 },
                        3: { targetAxisIndex: 1, color: '6AFFF3', lineDashStyle: [2, 2], lineWidth: 1 },
                        4: { targetAxisIndex: 1, color: 'BF71FF', lineDashStyle: [2, 2], lineWidth: 1 }
                    },
                    hAxis: {
                        title: 'Datetime',
                        format: 'dd/MM HH:mm',
                        titleTextStyle: { color: '#9193A8', italic: false },
                        textStyle: { color: '#9193A8', fontSize: 11 },
                        gridlines: { color: '#464859', count: 12 }
                    },
                    vAxis: {
                        titleTextStyle: { color: '#9193A8', italic: false },
                        textStyle: { color: '#9193A8', fontSize: 11 },
                        gridlines: { color: '#464859' }
                    },
                    vAxes: {
                        0: { ticks: [ 0, 100, 200, 300 ], title: 'Connexion speed (Mbps)' },
                        1: { ticks: [ 0,  50, 100, 150 ], title: 'Latency (ms)'           }
                    }
                };

                data.addColumn( 'datetime', 'Date'             );
                data.addColumn( 'number',   'Download'         );
                data.addColumn( 'number',   'Upload'           );
                data.addColumn( 'number',   'Ping'             );
                data.addColumn( 'number',   'Download latency' );
                data.addColumn( 'number',   'Upload latency'   );

                data.addRows( <?php echo $string_data_day; ?> );

                formatter_shortdate.format( data, 0 );
                
                chart.draw( data, options );
            }

            /* Draws the graph for Week's view. */
            function drawLinesChart_Week() {
                // Chart object.
                var chart = new google.visualization.LineChart( document.getElementById( 'chart_div_week' ) );

                // Data to be used for the chart.
                var data = new google.visualization.DataTable();

                // Format date values for x-axis.
                var formatter_shortdate = new google.visualization.DateFormat( { pattern: "dd/MM/yyyy KK:mm aa" } );

                // Chart settings.
                var options = {
                    title: 'SPEEDTEST Results (last week)',
                    titleTextStyle: { color: '#FFFFFF', fontSize: 18 },
                    chartArea: { backgroundColor: '#1A1B2E', left: 70, width: 580 },
                    backgroundColor: '#141526',
                    width:  720,
                    height: 360,
                    legend: { textStyle: { color: '#9193A8', fontSize: 11 }, position: 'top' },
                    focusTarget: 'category',
                    tooltip: { textStyle: { fontSize: 11 } },
                    series: {
                        0: { targetAxisIndex: 0, color: '6AFFF3' },
                        1: { targetAxisIndex: 0, color: 'BF71FF' },
                        2: { targetAxisIndex: 1, color: 'FFF38E', lineDashStyle: [2, 2], lineWidth: 1 },
                        3: { targetAxisIndex: 1, color: '6AFFF3', lineDashStyle: [2, 2], lineWidth: 1 },
                        4: { targetAxisIndex: 1, color: 'BF71FF', lineDashStyle: [2, 2], lineWidth: 1 }
                    },
                    hAxis: {
                        title: 'Datetime',
                        format: 'dd/MM HH:mm',
                        titleTextStyle: { color: '#9193A8', italic: false },
                        textStyle: { color: '#9193A8', fontSize: 11 },
                        gridlines: { color: '#464859', count: 12 }
                    },
                    vAxis: {
                        titleTextStyle: { color: '#9193A8', italic: false },
                        textStyle: { color: '#9193A8', fontSize: 11 },
                        gridlines: { color: '#464859' }
                    },
                    vAxes: {
                        0: { ticks: [ 0, 100, 200, 300 ], title: 'Connexion speed (Mbps)' },
                        1: { ticks: [ 0,  50, 100, 150 ], title: 'Latency (ms)'           }
                    }
                };

                data.addColumn( 'datetime', 'Date'             );
                data.addColumn( 'number',   'Download'         );
                data.addColumn( 'number',   'Upload'           );
                data.addColumn( 'number',   'Ping'             );
                data.addColumn( 'number',   'Download latency' );
                data.addColumn( 'number',   'Upload latency'   );

                data.addRows( <?php echo $string_data_week; ?> );
                
                formatter_shortdate.format( data, 0 );

                chart.draw( data, options );
            }

            /* Draws the graph for Month's view. */
            function drawLinesChart_Month() {
                // Chart object.
                var chart = new google.visualization.LineChart( document.getElementById( 'chart_div_month' ) );

                // Data to be used for the chart.
                var data = new google.visualization.DataTable();

                // Format date values for x-axis.
                var formatter_shortdate = new google.visualization.DateFormat( { pattern: "dd/MM/yyyy KK:mm aa" } );

                // Chart settings.
                var options = {
                    title: 'SPEEDTEST Results (last month)',
                    titleTextStyle: { color: '#FFFFFF', fontSize: 18 },
                    chartArea: { backgroundColor: '#1A1B2E', left: 70, width: 580 },
                    backgroundColor: '#141526',
                    width:  720,
                    height: 360,
                    legend: { textStyle: { color: '#9193A8', fontSize: 11 }, position: 'top' },
                    focusTarget: 'category',
                    tooltip: { textStyle: { fontSize: 11 } },
                    series: {
                        0: { targetAxisIndex: 0, color: '6AFFF3' },
                        1: { targetAxisIndex: 0, color: 'BF71FF' },
                        2: { targetAxisIndex: 1, color: 'FFF38E', lineDashStyle: [2, 2], lineWidth: 1 },
                        3: { targetAxisIndex: 1, color: '6AFFF3', lineDashStyle: [2, 2], lineWidth: 1 },
                        4: { targetAxisIndex: 1, color: 'BF71FF', lineDashStyle: [2, 2], lineWidth: 1 }
                    },
                    hAxis: {
                        title: 'Datetime',
                        format: 'dd/MM HH:mm',
                        titleTextStyle: { color: '#9193A8', italic: false },
                        textStyle: { color: '#9193A8', fontSize: 11 },
                        gridlines: { color: '#464859', count: 12 }
                    },
                    vAxis: {
                        titleTextStyle: { color: '#9193A8', italic: false },
                        textStyle: { color: '#9193A8', fontSize: 11 },
                        gridlines: { color: '#464859' }
                    },
                    vAxes: {
                        0: { ticks: [ 0, 100, 200, 300 ], title: 'Connexion speed (Mbps)' },
                        1: { ticks: [ 0,  50, 100, 150 ], title: 'Latency (ms)'           }
                    }
                };

                data.addColumn( 'datetime', 'Date'             );
                data.addColumn( 'number',   'Download'         );
                data.addColumn( 'number',   'Upload'           );
                data.addColumn( 'number',   'Ping'             );
                data.addColumn( 'number',   'Download latency' );
                data.addColumn( 'number',   'Upload latency'   );

                data.addRows( <?php echo $string_data_month; ?> );
                
                formatter_shortdate.format( data, 0 );
                
                chart.draw( data, options );
            }
        </script>
    </head>

    <body>
        <!-- <div class="tab">
            <button class="tablinks" onclick="showTabView(event, 'Last')" id="defaultTab"> Last </button>
            <button class="tablinks" onclick="showTabView(event, 'Day')"> Day </button>
            <button class="tablinks" onclick="showTabView(event, 'Week')"> Week </button>
            <button class="tablinks" onclick="showTabView(event, 'Month')"> Month </button>
        </div> -->

        <div id="Last" class="tabcontent">
            <table border=0 width=720 height=360 bgcolor="#141526">
                <tr align="center" valign="bottom"> <td colspan=2> <a style="color:#1BB3EF; font-size:16px"> <?php echo $last_timestamp; ?> </a> </td> </tr>
                <tr align="center" valign="bottom">
                    <td> <a style="color:#FFFFFF; font-size:18px"> DOWNLOAD </a> <a style="color:#9193A8; font-size:18px"> Mbps </a> </td>
                    <td> <a style="color:#FFFFFF; font-size:18px"> UPLOAD   </a> <a style="color:#9193A8; font-size:18px"> Mbps </a> </td>
                </tr>
                <tr valign="top" align="center">
                    <td> <a style="color:#FFFFFF; font-size:54px"> <?php echo $last_download_bandwith; ?> </a> </td>
                    <td> <a style="color:#FFFFFF; font-size:54px"> <?php echo $last_upload_bandwith; ?>   </a> </td>
                </tr>
                <tr valign="top">
                    <td colspan=2 align="center" style="color:#FFFFFF; font-size:16px">
                        <a> Ping:             </a> <a style="color:#FFF38E"> <?php echo $last_ping_latency; ?>         </a> <a style="color:#9193A8"> ms </a> <br>
                        <a> Download latency: </a> <a style="color:#6AFFF3"> <?php echo $last_download_latency_iqm; ?> </a> <a style="color:#9193A8"> ms </a> <br>
                        <a> Upload latency:   </a> <a style="color:#BF71FF"> <?php echo $last_upload_latency_iqm; ?>   </a> <a style="color:#9193A8"> ms </a>
                    </td>
                </tr>
                <tr align="center">
                    <td colspan=2> <a href="<?php echo $last_result_url; ?>" target="_blank" style="color:#1BB3EF; font-size:16px"> >> Click here to see this result in speedtest.net  <<</a> </td>
                </tr>
            </table>
        </div>
        <br>
        <div id="Day" class="tabcontent">
            <div id="chart_div_day"></div>
        </div>
        <br>
        <div id="Week" class="tabcontent">
            <div id="chart_div_week"></div>
        </div>
        <br>
        <div id="Month" class="tabcontent">
            <div id="chart_div_month"></div>
        </div>

        <!-- <script type="text/javascript">
            function showTabView( evt, viewName ) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName( "tabcontent" );

                for( i = 0; i < tabcontent.length; i++ ) {
                    tabcontent[i].style.display = "none";
                }

                tablinks = document.getElementsByClassName( "tablinks" );

                for( i = 0; i < tablinks.length; i++ ) {
                    tablinks[i].className = tablinks[i].className.replace( " active", "" );
                }

                document.getElementById( viewName ).style.display = "block";
                evt.currentTarget.className += " active";
            }

            /* Show the "defaultTab" element. */
            document.getElementById( "defaultTab" ).click();
        </script> -->
    </body>
</html>