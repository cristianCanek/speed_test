<?php require "database.php"; ?>

<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load('current', {'packages':['gauge']});
            google.charts.load( 'current', { packages: [ 'corechart', 'line' ] } );

            google.charts.setOnLoadCallback( drawLinesChart_LastDownload );
            google.charts.setOnLoadCallback( drawLinesChart_LastUpload );
            google.charts.setOnLoadCallback( drawLinesChart_Today );
            google.charts.setOnLoadCallback( drawLinesChart_Week );
            google.charts.setOnLoadCallback( drawLinesChart_Month );

            /* Draws the donwload graph for Last's view. */
            function drawLinesChart_LastDownload() {
                var data = google.visualization.arrayToDataTable( [
                    [ 'Label', 'Value'  ],
                    [ 'Download', <?php echo $lst_download; ?> ]
                ]);

                var options = {
                    min:          0,
                    max:         50,
                    width:      400,
                    height:     120,
                    redFrom:      0,
                    redTo:       10,
                    yellowFrom:  10,
                    yellowTo:    15,
                    greenFrom:   15,
                    greenTo:     50,
                    minorTicks:   5,
                    majorTicks: ['0', '10', '20', '30', '40', '50']
                };

                var chart = new google.visualization.Gauge( document.getElementById( 'chart_div_last_download' ) );

                chart.draw(data, options);
            }

            /* Draws the upload graph for Last's view. */
            function drawLinesChart_LastUpload() {
                var data = google.visualization.arrayToDataTable( [
                    [ 'Label', 'Value'  ],
                    [ 'Upload', <?php echo $lst_upload; ?> ]
                ]);

                var options = {
                    min:          0,
                    max:         50,
                    width:      400,
                    height:     120,
                    redFrom:      0,
                    redTo:        1,
                    yellowFrom:   1,
                    yellowTo:     2,
                    greenFrom:    2,
                    greenTo:     50,
                    minorTicks:   5,
                    majorTicks: ['0', '10', '20', '30', '40', '50']
                };

                var chart = new google.visualization.Gauge( document.getElementById( 'chart_div_last_upload' ) );

                chart.draw(data, options);
            }

            /* Draws the graph for Today's view. */
            function drawLinesChart_Today() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

                data.addRows( <?php echo $string_data_today; ?> );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_today'));
                chart.draw(data, options);
            }

            /* Draws the graph for Week's view. */
            function drawLinesChart_Week() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

                data.addRows( <?php echo $string_data_week; ?> );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_week'));
                chart.draw(data, options);
            }

            /* Draws the graph for Month's view. */
            function drawLinesChart_Month() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

                data.addRows( <?php echo $string_data_month; ?> );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_month'));
                chart.draw(data, options);
            }
        </script>
    </head>

    <body>

        <div class="tab">
            <button class="tablinks" onclick="showTabView(event, 'Last')" id="defaultTab"> Last </button>
            <button class="tablinks" onclick="showTabView(event, 'Today')"> Today </button>
            <button class="tablinks" onclick="showTabView(event, 'Week')"> Week </button>
            <button class="tablinks" onclick="showTabView(event, 'Month')"> Month </button>
        </div>

        <div id="Last" class="tabcontent">
          <a> <?php echo $lst_timestamp; ?> </a> <br>
          <div id="chart_div_last_download"></div>
          <div id="chart_div_last_upload"></div>
          <br> <a> PING <?php echo $lst_ping; ?> ms</a> <br>
          <br> <a href="<?php echo $lst_result_url; ?>" target="_blank"> Ver en speedtest.net </a>
        </div>

        <div id="Today" class="tabcontent">
            <div id="chart_div_today"></div>
        </div>

        <div id="Week" class="tabcontent">
            <div id="chart_div_week"></div>
        </div>

        <div id="Month" class="tabcontent">
            <div id="chart_div_month"></div>
        </div>

        <script>
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
        </script>
    </body>
</html>
