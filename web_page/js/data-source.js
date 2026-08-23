// =============================================================================
// Temporary frontend data source.
//
// Alpha 4 intentionally exposes an asynchronous interface even though the data
// still arrives in the PHP-generated bootstrap payload. Alpha 5 can replace the
// implementation below with fetch() calls to the REST API while keeping app.js
// and charts.js largely unchanged.
// =============================================================================

(function() {
    "use strict";

    async function loadDashboardData() {
        if ( !window.speedTestBootstrap ) {
            throw new Error( "Dashboard bootstrap data is not available." );
        }

        return window.speedTestBootstrap;
    }

    window.SpeedTestDataSource = {
        loadDashboardData
    };
})();
