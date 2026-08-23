// =============================================================================
// Frontend application.
// =============================================================================

(function() {
    "use strict";

    function setText( elementId, value ) {
        const element = document.getElementById( elementId );

        if ( element ) {
            element.textContent = value;
        }
    }


    function renderLatestResult( result ) {
        const resultLink = document.getElementById( "last-result-link" );

        if ( !result ) {
            setText( "last-timestamp", "No measurements available" );
            return;
        }

        setText(
            "last-timestamp",
            SpeedTestCharts.formatDateTime( new Date( result.timestamp ).getTime() )
        );

        setText( "last-download",         Number( result.download_mbps ).toFixed( 2 ) );
        setText( "last-upload",           Number( result.upload_mbps ).toFixed( 2 ) );
        setText( "last-ping",             `${result.ping_ms} ms` );
        setText( "last-download-latency", `${result.download_latency} ms` );
        setText( "last-upload-latency",   `${result.upload_latency} ms` );

        if ( resultLink && result.result_url ) {
            resultLink.href   = result.result_url;
            resultLink.hidden = false;
        }
    }


    function renderCharts( ranges ) {
        SpeedTestCharts.createSpeedtestChart(
            "chart-day",
            ranges.day || [],
            {
                xTicksCount: 12
            }
        );

        SpeedTestCharts.createSpeedtestChart(
            "chart-week",
            ranges.week || [],
            {
                xTicksCount: 7
            }
        );

        SpeedTestCharts.createSpeedtestChart(
            "chart-month",
            ranges.month || [],
            {
                xTicksCount: 8
            }
        );
    }


    function showError( message ) {
        const banner = document.getElementById( "app-error" );
        const status = document.getElementById( "dashboard-status" );

        if ( banner ) {
            banner.textContent = message;
            banner.hidden      = false;
        }

        if ( status ) {
            status.textContent = "Dashboard error";
            status.classList.add( "status-badge--error" );
        }
    }


    async function initializeDashboard() {
        try {
            const data = await SpeedTestDataSource.loadDashboardData();

            renderLatestResult( data.last );
            renderCharts( data.ranges || {} );
        }
        catch ( error ) {
            console.error( error );
            showError( "Unable to load dashboard data. Check the browser console for details." );
        }
    }


    window.addEventListener( "DOMContentLoaded", initializeDashboard );
})();
