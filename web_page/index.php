<?php require "database.php"; ?>

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
