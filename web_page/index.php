<?php require "database.php"; ?>
<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="stylesheet.css">
        <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
        <script type="text/javascript">
            google.charts.load( 'current', { packages: [ 'corechart', 'line' ] } );
            google.charts.setOnLoadCallback( drawLinesChart_Last );
            google.charts.setOnLoadCallback( drawLinesChart_Today );
            google.charts.setOnLoadCallback( drawLinesChart_Weekly );
            google.charts.setOnLoadCallback( drawLinesChart_Monthly );

            /* Draws the graph for Last's view. */
            function drawLinesChart_Last() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_last'));
                chart.draw(data, options);
            }

            /* Draws the graph for Today's view. */
            function drawLinesChart_Today() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_today'));
                chart.draw(data, options);
            }

            /* Draws the graph for Weekly's view. */
            function drawLinesChart_Weekly() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_weekly'));
                chart.draw(data, options);
            }

            /* Draws the graph for Monthly's view. */
            function drawLinesChart_Monthly() {
                var data = new google.visualization.DataTable();

                data.addColumn( 'datetime', 'Date'     );
                data.addColumn( 'number',   'Download' );
                data.addColumn( 'number',   'Upload'   );

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

                var chart = new google.visualization.LineChart(document.getElementById('chart_div_monthly'));
                chart.draw(data, options);
            }
        </script>
    </head>

    <body>

        <div class="tab">
            <button class="tablinks" onclick="openCity(event, 'Last')" id="defaultTab">Last</button>
            <button class="tablinks" onclick="openCity(event, 'Today')">Today</button>
            <button class="tablinks" onclick="openCity(event, 'Weekly')">Weekly</button>
            <button class="tablinks" onclick="openCity(event, 'Monthly')">Monthly</button>
        </div>

        <div id="Last" class="tabcontent">
            <div id="chart_div_last"></div>
        </div>

        <div id="Today" class="tabcontent">
            <div id="chart_div_today"></div>
        </div>

        <div id="Weekly" class="tabcontent">
            <div id="chart_div_weekly"></div>
        </div>

        <div id="Monthly" class="tabcontent">
            <div id="chart_div_monthly"></div>
        </div>

        <script>
            function openCity(evt, cityName) {
                var i, tabcontent, tablinks;
                tabcontent = document.getElementsByClassName("tabcontent");

                for (i = 0; i < tabcontent.length; i++) {
                    tabcontent[i].style.display = "none";
                }

                tablinks = document.getElementsByClassName("tablinks");

                for (i = 0; i < tablinks.length; i++) {
                    tablinks[i].className = tablinks[i].className.replace(" active", "");
                }

                document.getElementById(cityName).style.display = "block";
                evt.currentTarget.className += " active";
            }

            /* Show the "defaultTab" element. */
            document.getElementById("defaultTab").click();
        </script>
    </body>
</html>
