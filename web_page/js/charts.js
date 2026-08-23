// =============================================================================
// Reusable Chart.js logic.
// =============================================================================

(function() {
    "use strict";

    const COLORS = {
        background:      "#1A1B2E",
        grid:            "#464859",
        text:            "#9193A8",
        title:           "#FFFFFF",
        download:        "#6AFFF3",
        upload:          "#BF71FF",
        ping:            "#FFF38E"
    };

    const chartInstances = new Map();


    // -------------------------------------------------------------------------
    // Formatting helpers.
    // -------------------------------------------------------------------------

    function pad2( value ) {
        return String( value ).padStart( 2, "0" );
    }


    function formatDateTime( timestamp, multiline = false ) {
        const date = new Date( timestamp );

        if ( multiline ) {
            return [
                pad2( date.getDate() ) + "/" + pad2( date.getMonth() + 1 ),
                pad2( date.getHours() ) + ":" + pad2( date.getMinutes() )
            ];
        }

        return (
            pad2( date.getDate() ) + "/" +
            pad2( date.getMonth() + 1 ) + "/" +
            date.getFullYear() + " " +
            pad2( date.getHours() ) + ":" +
            pad2( date.getMinutes() )
        );
    }


    function toPoints( rows, valueIndex ) {
        return rows.map( row => ({
            x: new Date( row[0] ).getTime(),
            y: Number( row[valueIndex] )
        }) );
    }


    function getMinTimestamp( rows ) {
        if ( rows.length === 0 ) {
            return undefined;
        }

        return new Date( rows[0][0] ).getTime();
    }


    function getMaxTimestamp( rows ) {
        if ( rows.length === 0 ) {
            return undefined;
        }

        return new Date( rows[rows.length - 1][0] ).getTime();
    }


    // -------------------------------------------------------------------------
    // Chart.js plugin.
    // -------------------------------------------------------------------------

    // Google Charts allowed separate colors for the chart background
    // and plot area. This small plugin preserves the same visual idea.
    const chartAreaBackground = {
        id: "chartAreaBackground",

        beforeDraw( chart, args, options ) {
            const { ctx, chartArea } = chart;

            if ( !chartArea ) {
                return;
            }

            ctx.save();
            ctx.fillStyle = options.color || COLORS.background;
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


    // -------------------------------------------------------------------------
    // Chart creation.
    // -------------------------------------------------------------------------

    function createDataset( label, rows, valueIndex, axis, color, dashed = false ) {
        return {
            label,
            data:             toPoints( rows, valueIndex ),
            yAxisID:          axis,
            borderColor:      color,
            backgroundColor:  color,
            borderDash:       dashed ? [ 2, 2 ] : undefined,
            borderWidth:      dashed ? 1 : 2,
            pointRadius:      0,
            pointHoverRadius: 3
        };
    }


    function createSpeedtestChart( canvasId, rows, options = {} ) {
        const canvas = document.getElementById( canvasId );

        if ( !canvas ) {
            throw new Error( `Chart canvas '${canvasId}' was not found.` );
        }

        const previousChart = chartInstances.get( canvasId );

        if ( previousChart ) {
            previousChart.destroy();
        }

        const minTimestamp = getMinTimestamp( rows );
        const maxTimestamp = getMaxTimestamp( rows );

        const chart = new Chart( canvas, {
            type: "line",

            data: {
                datasets: [
                    createDataset( "Download",         rows, 1, "ySpeed",   COLORS.download ),
                    createDataset( "Upload",           rows, 2, "ySpeed",   COLORS.upload ),
                    createDataset( "Ping",             rows, 3, "yLatency", COLORS.ping,     true ),
                    createDataset( "Download latency", rows, 4, "yLatency", COLORS.download, true ),
                    createDataset( "Upload latency",   rows, 5, "yLatency", COLORS.upload,   true )
                ]
            },

            options: {
                responsive:          true,
                maintainAspectRatio: false,
                parsing:             false,
                normalized:          true,

                interaction: {
                    mode:      "index",
                    intersect: false
                },

                plugins: {
                    chartAreaBackground: {
                        color: COLORS.background
                    },

                    legend: {
                        position: "top",
                        labels: {
                            color:     COLORS.text,
                            boxWidth:  18,
                            boxHeight: 2,
                            usePointStyle: false,
                            font: {
                                size: 11
                            }
                        }
                    },

                    tooltip: {
                        callbacks: {
                            title( items ) {
                                if ( items.length === 0 ) {
                                    return "";
                                }

                                return formatDateTime( items[0].parsed.x );
                            }
                        }
                    }
                },

                scales: {
                    x: {
                        type:   "linear",
                        bounds: "data",
                        offset: false,
                        min:    minTimestamp,
                        max:    maxTimestamp,

                        title: {
                            display: true,
                            text:    "Datetime",
                            color:   COLORS.text
                        },

                        ticks: {
                            color: COLORS.text,
                            count: options.xTicksCount,

                            font: {
                                size: 11
                            },

                            callback( value ) {
                                return formatDateTime( value, true );
                            }
                        },

                        grid: {
                            color: COLORS.grid
                        }
                    },

                    ySpeed: {
                        type:         "linear",
                        position:     "left",
                        beginAtZero:  true,
                        suggestedMax: 600,

                        title: {
                            display: true,
                            text:    "Connection speed (Mbps)",
                            color:   COLORS.text
                        },

                        ticks: {
                            color: COLORS.text,
                            count: 5
                        },

                        grid: {
                            color: COLORS.grid
                        }
                    },

                    yLatency: {
                        type:         "linear",
                        position:     "right",
                        beginAtZero:  true,
                        suggestedMax: 150,

                        title: {
                            display: true,
                            text:    "Latency (ms)",
                            color:   COLORS.text
                        },

                        ticks: {
                            color: COLORS.text,
                            count: 5
                        },

                        grid: {
                            drawOnChartArea: false
                        }
                    }
                }
            }
        } );

        chartInstances.set( canvasId, chart );

        return chart;
    }


    function destroyAll() {
        chartInstances.forEach( chart => chart.destroy() );
        chartInstances.clear();
    }


    window.SpeedTestCharts = {
        createSpeedtestChart,
        destroyAll,
        formatDateTime
    };
})();
