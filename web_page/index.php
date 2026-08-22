<?php require "database.php"; ?>

<!DOCTYPE html>
<html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" type="text/css" href="stylesheet.css">

        <!-- Chart.js is bundled locally so the dashboard remains functional without WAN access. -->
        <script type="text/javascript" src="js/vendor/chart.umd.min.js"></script>

        <script type="text/javascript">
            // -----------------------------------------------------------------
            // PHP-generated datasets.
            // -----------------------------------------------------------------

            const dataDay   = <?php echo $string_data_day;   ?>;
            const dataWeek  = <?php echo $string_data_week;  ?>;
            const dataMonth = <?php echo $string_data_month; ?>;


            // -----------------------------------------------------------------
            // Chart.js helpers.
            // -----------------------------------------------------------------

            // Pad a number to 2 digits with leading zeros.
            function pad2( value ) {
                return String( value ).padStart( 2, '0' );
            }


            // Format a timestamp into a human-readable date and time string.
            // If multiline is true, the date and time are returned on separate lines.
            function formatDateTime( timestamp, multiline = false ) {
                const date = new Date( timestamp );

                if ( multiline ) {
                    return (
                        [
                            pad2( date.getDate()      ) + '/' + pad2( date.getMonth() + 1 ),
                            pad2( date.getHours()     ) + ':' + pad2( date.getMinutes()   )
                        ]
                    );
                }
                
                return (
                    pad2( date.getDate()      ) + '/' +
                    pad2( date.getMonth() + 1 ) + '/' +
                    pad2( date.getFullYear()  ) + ' ' +
                    pad2( date.getHours()     ) + ':' +
                    pad2( date.getMinutes()   )
                );
            }


            // Convert an array of rows into an array of points for Chart.js.
            function toPoints( rows, valueIndex ) {
                return rows.map( row => ({
                    x: new Date( row[0] ).getTime(),
                    y: Number( row[valueIndex] )
                }) );
            }


            // Get the first timestamp in a dataset.
            function getMinTimestamp( rows ) {
                if ( rows.length === 0 ) {
                    return undefined;
                }

                return new Date( rows[0][0] ).getTime();
            }


            // Get the last timestamp in a dataset.
            function getMaxTimestamp( rows ) {
                if ( rows.length === 0 ) {
                    return undefined;
                }

                return new Date( rows[rows.length - 1][0] ).getTime();
            }


            // Google Charts allowed separate colors for the chart background
            // and plot area. This small plugin preserves the same visual idea.
            const chartAreaBackground = {
                id: 'chartAreaBackground',

                beforeDraw( chart, args, options ) {
                    const { ctx, chartArea } = chart;

                    if ( !chartArea ) {
                        return;
                    }

                    ctx.save();
                    ctx.fillStyle = options.color || '#1A1B2E';
                    ctx.fillRect(
                        chartArea.left,
                        chartArea.top,
                        chartArea.right - chartArea.left,
                        chartArea.bottom - chartArea.top
                    );
                    ctx.restore();
                }
            };

            Chart.register( chartAreaBackground );


            // Create a Chart.js line chart for speedtest results.
            function createSpeedtestChart( canvasId, title, rows, xTicksLimit, xStepMs = undefined ) {
                const canvas       = document.getElementById( canvasId );
                const minTimestamp = getMinTimestamp( rows );
                const maxTimestamp = getMaxTimestamp( rows );

                new Chart( canvas, {
                    type: 'line',

                    data: {
                        datasets: [
                            {
                                label:           'Download',
                                data:             toPoints( rows, 1 ),
                                yAxisID:          'ySpeed',
                                borderColor:      '#6AFFF3',
                                backgroundColor:  '#6AFFF3',
                                borderWidth:      2,
                                pointRadius:      0,
                                pointHoverRadius: 3
                            },
                            {
                                label:           'Upload',
                                data:             toPoints( rows, 2 ),
                                yAxisID:          'ySpeed',
                                borderColor:      '#BF71FF',
                                backgroundColor:  '#BF71FF',
                                borderWidth:      2,
                                pointRadius:      0,
                                pointHoverRadius: 3
                            },
                            {
                                label:           'Ping',
                                data:             toPoints( rows, 3 ),
                                yAxisID:          'yLatency',
                                borderColor:      '#FFF38E',
                                backgroundColor:  '#FFF38E',
                                borderDash:       [ 2, 2 ],
                                borderWidth:      1,
                                pointRadius:      0,
                                pointHoverRadius: 3
                            },
                            {
                                label:           'Download latency',
                                data:             toPoints( rows, 4 ),
                                yAxisID:          'yLatency',
                                borderColor:      '#6AFFF3',
                                backgroundColor:  '#6AFFF3',
                                borderDash:       [ 2, 2 ],
                                borderWidth:      1,
                                pointRadius:      0,
                                pointHoverRadius: 3
                            },
                            {
                                label:           'Upload latency',
                                data:             toPoints( rows, 5 ),
                                yAxisID:          'yLatency',
                                borderColor:      '#BF71FF',
                                backgroundColor:  '#BF71FF',
                                borderDash:       [ 2, 2 ],
                                borderWidth:      1,
                                pointRadius:      0,
                                pointHoverRadius: 3
                            }
                        ]
                    },

                    options: {
                        responsive:          false,
                        maintainAspectRatio: false,
                        parsing:             false,

                        interaction: {
                            mode:      'index',
                            intersect: false
                        },

                        plugins: {
                            chartAreaBackground: { color: '#1A1B2E' },

                            title: {
                                display: true,
                                text:    title,
                                color:   '#FFFFFF',
                                font:    { size: 18 }
                            },

                            legend: {
                                position: 'top',
                                labels: {
                                    color: '#9193A8',
                                    font:  { size: 11 }
                                }
                            },

                            tooltip: {
                                callbacks: {
                                    title( items ) {
                                        if ( items.length === 0 ) {
                                            return '';
                                        }

                                        return formatDateTime( items[0].parsed.x );
                                    }
                                }
                            }
                        },

                        scales: {
                            x: {
                                type:   'linear',
                                bounds: 'data',
                                offset: false,
                                min:    minTimestamp,
                                max:    maxTimestamp,

                                title: {
                                    display: true,
                                    text:    'Datetime',
                                    color:   '#9193A8'
                                },

                                ticks: {
                                    color: '#9193A8',
                                    font:  { size: 11 },
                                    maxTicksLimit: xTicksLimit,
                                    stepSize:      xStepMs,

                                    callback( value ) {
                                        return formatDateTime( value, true );
                                    }
                                },

                                grid: { color: '#464859' }
                            },

                            ySpeed: {
                                type:         'linear',
                                position:     'left',
                                beginAtZero:  true,
                                suggestedMax: 600,

                                title: {
                                    display: true,
                                    text:    'Connexion speed (Mbps)',
                                    color:   '#9193A8'
                                },

                                ticks: {
                                    color:    '#9193A8',
                                    count: 5
                                },

                                grid: { color: '#464859' }
                            },

                            yLatency: {
                                type:         'linear',
                                position:     'right',
                                beginAtZero:  true,
                                suggestedMax: 150,

                                title: {
                                    display: true,
                                    text:    'Latency (ms)',
                                    color:   '#9193A8'
                                },

                                ticks: {
                                    color: '#9193A8',
                                    count: 5
                                },

                                grid: { drawOnChartArea: false }
                            }
                        }
                    }
                } );
            }

            window.addEventListener( 'DOMContentLoaded', function() {
                const TWO_HOURS_MS = 2 * 60 * 60 * 1000;

                createSpeedtestChart( 'chart_div_day',   'SPEEDTEST Results (last 24 hrs)', dataDay,   13, TWO_HOURS_MS   );
                createSpeedtestChart( 'chart_div_week',  'SPEEDTEST Results (last week)',   dataWeek,  7                  );
                createSpeedtestChart( 'chart_div_month', 'SPEEDTEST Results (last month)',  dataMonth, 8                  );
            } );
        </script>
    </head>

    <body>
         <div id="Last" class="tabcontent">
            <table border=0 width=720 height=360 bgcolor="#141526">
                <tr align="center" valign="bottom"> <td colspan=2> <a style="color:#1BB3EF; font-size:16px"> <?php echo $last_timestamp; ?> </a> </td> </tr>
                <tr align="center" valign="bottom">
                    <td> <a style="color:#FFFFFF; font-size:18px"> DOWNLOAD </a> <a style="color:#9193A8; font-size:18px"> Mbps </a> </td>
                    <td> <a style="color:#FFFFFF; font-size:18px"> UPLOAD   </a> <a style="color:#9193A8; font-size:18px"> Mbps </a> </td>
                </tr>
                <tr valign="top" align="center">
                    <td> <a style="color:#FFFFFF; font-size:54px"> <?php echo $last_download_bandwith; ?> </a> </td>
                    <td> <a style="color:#FFFFFF; font-size:54px"> <?php echo $last_upload_bandwith;   ?> </a> </td>
                </tr>
                <tr valign="top">
                    <td colspan=2 align="center" style="color:#FFFFFF; font-size:16px">
                        <a> Ping:             </a> <a style="color:#FFF38E"> <?php echo $last_ping_latency;         ?> </a> <a style="color:#9193A8"> ms </a> <br>
                        <a> Download latency: </a> <a style="color:#6AFFF3"> <?php echo $last_download_latency_iqm; ?> </a> <a style="color:#9193A8"> ms </a> <br>
                        <a> Upload latency:   </a> <a style="color:#BF71FF"> <?php echo $last_upload_latency_iqm;   ?> </a> <a style="color:#9193A8"> ms </a>
                    </td>
                </tr>
                <tr align="center">
                    <td colspan=2> <a href="<?php echo $last_result_url; ?>" target="_blank" style="color:#1BB3EF; font-size:16px"> >> Click here to see this result in speedtest.net  <<</a> </td>
                </tr>
            </table>
        </div>
        <div id="Day" class="tabcontent">
            <canvas id="chart_div_day" width="720" height="360" style="background-color:#141526"> </canvas>
        </div>
        <div id="Week" class="tabcontent">
            <canvas id="chart_div_week" width="720" height="360" style="background-color:#141526"> </canvas>
        </div>
        <div id="Month" class="tabcontent">
            <canvas id="chart_div_month" width="720" height="360" style="background-color:#141526"> </canvas>
        </div>
    </body>
</html>
