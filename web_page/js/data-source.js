// =============================================================================
// REST API data source.
// =============================================================================

(function() {
    "use strict";

    // Fetch JSON data from the given URL, throwing an error if the request fails.
    async function requestJson( url, options = {} ) {
        const response = await fetch( url, {
            headers: {
                "Accept": "application/json"
            },
            ...options
        } );

        if ( !response.ok ) {
            let detail = `${response.status} ${response.statusText}`;

            try {
                const body = await response.json();

                if ( body.detail ) {
                    detail = body.detail;
                }
            }
            catch ( error ) {
                // Keep the HTTP status text when the response is not JSON.
            }

            throw new Error( `Request to '${url}' failed: ${detail}` );
        }

        return response.json();
    }


    // Convert the results to a format suitable for charting.
    function toChartRows( results ) {
        return results.map( result => [
            result.timestamp,
            result.download_mbps,
            result.upload_mbps,
            result.ping_ms,
            result.download_latency,
            result.upload_latency
        ] );
    }


    // Render the last result on the dashboard.
    async function loadDashboardData() {
        const [
            status,
            day,
            week,
            month
        ] = await Promise.all( [
            requestJson( "/api/v1/status" ),
            requestJson( "/api/v1/results?range=24h" ),
            requestJson( "/api/v1/results?range=7d"  ),
            requestJson( "/api/v1/results?range=30d" )
        ] );

        return {
            last: status.last_result,
            ranges: {
                day:   toChartRows( day.results   ),
                week:  toChartRows( week.results  ),
                month: toChartRows( month.results )
            }
        };
    }


    // Load results for a specific time range.
    async function loadResults( range ) {
        return requestJson(
            `/api/v1/results?range=${encodeURIComponent( range )}`
        );
    }


    // Load statistics for a specific time range.
    async function loadStatistics( range ) {
        return requestJson(
            `/api/v1/statistics?range=${encodeURIComponent( range )}`
        );
    }


    // Load configuration data from the server.
    async function loadConfig() {
        return requestJson( "/api/v1/config" );
    }


    //  Load the status of the speed_test service.
    async function loadStatus() {
        return requestJson( "/api/v1/status" );
    }


    window.SpeedTestDataSource = {
        loadDashboardData,
        loadResults,
        loadStatistics,
        loadConfig,
        loadStatus
    };
})();
