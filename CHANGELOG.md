# Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

Development plans and upcoming milestones are documented separately in [ROADMAP.md](ROADMAP.md).


## Table of Contents

- [[v2.0.0-alpha.7] - 2026-08-25](#v200-alpha7---2026-08-25)
- [[v2.0.0-alpha.6] - 2026-08-25](#v200-alpha6---2026-08-25)
- [[v2.0.0-alpha.5] - 2026-08-23](#v200-alpha5---2026-08-23)
- [[v2.0.0-alpha.4] - 2026-08-23](#v200-alpha4---2026-08-23)
- [[v2.0.0-alpha.3] - 2026-08-21](#v200-alpha3---2026-08-21)
- [[v2.0.0-alpha.2] - 2026-08-20](#v200-alpha2---2026-08-20)
- [[v2.0.0-alpha.1] - 2026-08-20](#v200-alpha1---2026-08-20)
- [[v1.0.0] - 2026-08-19](#v100---2026-08-19)


## [Unreleased]

No unreleased changes yet.


## [v2.0.0-alpha.7] - 2026-08-25

Seventh functional development milestone toward Version 2.


### Added

- Added reusable `SpeedtestCollector` orchestration.
- Added dedicated Ookla CLI execution layer.
- Added dedicated JSON parsing and validation layer.
- Added typed collector/domain models for measurements and execution outcomes.
- Added dedicated collector database repository.
- Added collector command-line entry point through `python -m collector`.
- Added manual Speedtest execution through `docker exec`.
- Added `--save` for persistent manual executions.
- Added `--raw-json` for raw Ookla JSON output.
- Added timeout handling for Ookla CLI execution.
- Added explicit handling for missing CLI executable and non-zero exit codes.
- Added validation for empty, invalid, and malformed Ookla JSON output.
- Added shared cross-container lock at `/config/data/speedtest.lock`.
- Added persistent collector/runtime logging at `/config/logs/collector.log`.
- Added shared logging configuration in `app/logging_config.py`.
- Added structured logger hierarchy for `speed_test.collector`, `speed_test.scheduler`, and `speed_test.database`.
- Added functional `POST /api/v1/tests/run` manual Speedtest execution.
- Added REST request options for persistence and raw output.


### Changed

- Replaced the monolithic `app/collector/speedtest.py` implementation with a reusable collector package.
- Changed scheduled execution to call the same `SpeedtestCollector` used by manual and REST-triggered tests.
- Changed CLI execution from combined-output `check_output()` behavior to explicit stdout/stderr/exit-code handling.
- Changed diagnostic console logging to stderr so stdout remains suitable for machine-readable command output.
- Changed database startup/migration messages from unstructured `print()` output to shared component logging.
- Changed scheduler lifecycle messages to use the `speed_test.scheduler` logger.
- Changed collector execution messages to use the `speed_test.collector` logger.
- Changed the lock file from a container-local temporary path to shared persistent state so both Alpha 7 containers coordinate execution.
- Included the reusable collector package and Ookla CLI in the FastAPI application image to prepare the Alpha 8 single-container merge.


### REST API

- Implemented `POST /api/v1/tests/run`.
- Added `save` request option to control persistence of both successful and failed manual executions.
- Added `raw` request option to include the original Ookla stdout payload.
- Kept scheduled and REST-triggered execution behavior behind the same collector implementation.


### Validation

- Verified scheduled Speedtests continue to execute and persist successfully.
- Verified manual non-persistent execution through Docker exec.
- Verified manual persistent execution through Docker exec.
- Verified raw Ookla JSON output.
- Verified combined persistent + raw execution.
- Verified machine-readable stdout with diagnostic logging separated to stderr.
- Verified REST `save=false, raw=false`.
- Verified REST `save=true, raw=false`.
- Verified REST `save=false, raw=true`.
- Verified cross-container overlap protection and `missing / overlap` reporting.
- Verified missing CLI handling through `failed / cli_not_found`.
- Verified timeout handling through `failed / timeout`.
- Verified timeout with `save=false` is not persisted.
- Verified timeout with `save=true` is persisted as a failed execution.
- Verified scheduled timeout failures are persisted.
- Verified persistent logging contains scheduled, manual, and API execution events.
- Verified component-level logging for database, scheduler, and collector messages.
- Verified the existing Version 2 database migration and dashboard/API behavior remain operational.


### Documentation

- Updated the README with the Alpha 7 reusable collector architecture.
- Documented manual collector execution and persistence/raw-output options.
- Documented the shared lock and persistent logging behavior.
- Marked `v2.0.0-alpha.7` as completed in the roadmap.


## [v2.0.0-alpha.6] - 2026-08-25

Sixth functional development milestone toward Version 2.


### Added

- Added the Version 2 SQLite schema.
- Added explicit database schema-version tracking through `schema_version`.
- Added automatic Version 1 ? Version 2 migration through `001_v1_to_v2.sql`.
- Added `speedtest_runs` as the Version 2 execution/measurement table.
- Added normalized Version 2 column names and explicit measurement units.
- Added indexes for timestamp, status/timestamp, and result-ID queries.
- Added persistent `success`, `failed`, and `missing` execution states.
- Added persistent error type, error message, and exit-code fields.
- Added migration traceability through `legacy_raw_result_id`.
- Added statistics counts for successful, failed, and missing executions.
- Added a dashboard link to the interactive REST API documentation.


### Changed

- Changed fresh database initialization to create schema version 2 directly.
- Changed collector inserts from the legacy `rawResults` schema to `speedtest_runs`.
- Changed REST API database queries to use the Version 2 schema.
- Changed statistics queries to operate on Version 2 execution states.
- Changed timestamp persistence to a consistent UTC representation.
- Changed scheduler status presentation so `next_scheduled_boundary` uses the IANA timezone configured in `settings.yaml`.
- Kept stored measurement timestamps in UTC.
- Kept the existing `/api/v1` response contract used by the dashboard.


### Migration

- Existing supported Version 1 databases are detected automatically.
- Historical Version 1 measurements are copied into the Version 2 schema.
- Migrated Version 1 measurements are represented as successful executions.
- Original Version 1 row identifiers are preserved in `legacy_raw_result_id`.
- Legacy Version 1 tables/views remain in place during Alpha 6 as a safety measure.


### Validation

- Verified creation of a new schema-version-2 database from an empty persistent-data directory.
- Verified the initial `schema_version` record for a fresh database.
- Verified successful scheduled measurements are stored in `speedtest_runs`.
- Verified invalid Speedtest output is stored as a failed execution with error information.
- Verified the REST API reads successful Version 2 measurements.
- Verified `/health` remains healthy with the Version 2 database.
- Verified the dashboard and historical charts render after the persistence-layer change.
- Verified Version 1 ? Version 2 migration using a copy of the production database.
- Verified the migrated historical-row count matches the Version 1 source-row count.
- Verified the existing historical dataset remains queryable after migration.
- Verified the next scheduler boundary is returned using the configured timezone.
- Verified the REST API documentation link opens `/docs` in a separate browser tab.


### Documentation

- Updated the README with the Version 2 database model, migration behavior, and current Alpha 6 architecture.
- Marked `v2.0.0-alpha.6` as completed in the roadmap.
- Documented automatic Version 1 ? Version 2 migration and the preservation of legacy objects during Alpha 6.


## [v2.0.0-alpha.5] - 2026-08-23

Fifth functional development milestone toward Version 2.


### Added

- Added FastAPI as the Version 2 application backend.
- Added Uvicorn as the ASGI server.
- Added public API versioning under `/api/v1`.
- Added `/health` for application/database health.
- Added `/api/v1/status` for scheduler and latest-result information.
- Added `/api/v1/results` with dynamic hour/day/all ranges.
- Added `/api/v1/statistics` with average, median, minimum, and maximum statistics.
- Added `/api/v1/config` for public non-sensitive configuration.
- Added the reserved `POST /api/v1/tests/run` endpoint.
- Added a dedicated read-only SQLite query layer for the application backend.
- Added interactive OpenAPI/Swagger documentation at `/docs`.
- Added OpenAPI schema generation at `/openapi.json`.
- Added a dedicated FastAPI application Docker image.


### Changed

- Changed the frontend data source from the PHP bootstrap payload to public REST API `fetch()` requests.
- Changed the frontend entry point from `index.php` to static `index.html`.
- Changed static frontend serving from Nginx to FastAPI/Starlette.
- Changed the active runtime architecture from three containers to two.
- Changed the application container to expose Uvicorn internally while Docker Compose maps it to host port `8000`.
- Preserved the collector as a separate persistent container for scheduled execution.
- Preserved the existing Version 1-compatible SQLite schema during this milestone.


### Removed

- Removed PHP from the active runtime after its database-read responsibilities were replaced.
- Removed Nginx from the active runtime after FastAPI took over static frontend serving.
- Removed the frontend's dependency on PHP-generated markup/data bootstrap.


### Validation

- Verified exactly two active containers: collector and application.
- Verified the dashboard loads through FastAPI and consumes the public REST API.
- Verified `/health` returns HTTP `200` with database status.
- Verified `/api/v1/status`.
- Verified `/api/v1/results?range=24h`.
- Verified `/api/v1/results?range=7d`.
- Verified dynamic ranges including `3h`, `14d`, and `all`.
- Verified the full historical dataset can be returned through `range=all`.
- Verified `/api/v1/statistics?range=24h`.
- Verified `/api/v1/config`.
- Verified invalid and excessive ranges return HTTP `400`.
- Verified interactive API documentation at `/docs`.
- Verified `POST /api/v1/tests/run` returns the expected HTTP `501` placeholder response.


### Documentation

- Updated the README with the Alpha 5 FastAPI/REST architecture and endpoint reference.
- Marked `v2.0.0-alpha.5` as completed in the Version 2 roadmap.
- Documented that `/docs` is the Swagger/OpenAPI UI path and that the manual-test route is a `POST` operation.
- Kept the Alpha 9 plan to install and pin Ookla Speedtest CLI from Ookla's Debian/Ubuntu package repository and validate JSON compatibility before replacing the current CLI.


## [v2.0.0-alpha.4] - 2026-08-23

Fourth functional development milestone toward Version 2.


### Added

- Added semantic HTML dashboard structure for the latest measurement and historical charts.
- Added responsive CSS based on CSS Grid and Flexbox.
- Added responsive Chart.js containers for desktop, tablet, and mobile layouts.
- Added `web_page/js/app.js` for dashboard presentation and rendering.
- Added `web_page/js/charts.js` for reusable Chart.js logic.
- Added `web_page/js/data-source.js` as an asynchronous frontend data-source abstraction.
- Added a local SVG favicon.
- Added a browser page title for the dashboard.


### Changed

- Separated frontend presentation from PHP-generated markup.
- Changed PHP to produce a single JSON-compatible bootstrap payload instead of rendering individual presentation values directly into the page.
- Replaced the table-based latest-result layout with responsive metric cards.
- Moved Chart.js configuration and helper functions out of `index.php`.
- Made Chart.js rendering responsive while preserving the existing 24-hour, weekly, and monthly datasets.
- Preserved local/offline frontend assets and the existing three-container runtime architecture.
- Prepared the frontend data-loading contract for REST API consumption in Alpha 5.


### Validation

- Verified the latest download and upload values render correctly.
- Verified ping, download latency, and upload latency render correctly.
- Verified the Speedtest.net result link remains functional.
- Verified 24-hour, weekly, and monthly charts render correctly.
- Verified charts resize with the responsive dashboard layout.
- Verified the dashboard remains usable across desktop and narrower viewport widths.
- Verified the local Chart.js runtime continues to operate without WAN access.
- Verified the favicon and browser title load locally.


### Documentation

- Updated the README with the Alpha 4 frontend architecture and module responsibilities.
- Marked `v2.0.0-alpha.4` as completed in the Version 2 roadmap.
- Updated the Alpha 9 packaging plan to install a pinned Ookla Speedtest CLI package from Ookla's Debian/Ubuntu repository.
- Added an Alpha 9 validation step for Ookla CLI JSON compatibility before replacing the currently bundled executable.


## [v2.0.0-alpha.3] - 2026-08-21

Third functional development milestone toward Version 2.


### Added

- Added Chart.js as the local dashboard charting library.
- Added the vendored Chart.js UMD runtime under `web_page/js/vendor/`.
- Added local frontend asset delivery through the existing Nginx container.
- Added JSON-compatible PHP-generated datasets for Chart.js.
- Added reusable JavaScript helpers for chart data conversion and date formatting.


### Changed

- Replaced Google Charts rendering with Chart.js.
- Changed the 24-hour, weekly, and monthly charts to consume the same existing historical datasets through Chart.js.
- Changed chart X-axis scaling so datasets span the full available chart width.
- Updated Nginx and PHP image packaging to include the current frontend files and local JavaScript assets.
- Preserved the current PHP backend, SQLite schema, collector behavior, and three-container architecture.


### Removed

- Removed the Google Charts frontend runtime dependency.
- Removed the need for an external chart/CDN connection during dashboard runtime.


### Validation

- Verified the latest-result view continues to render.
- Verified the 24-hour chart renders correctly.
- Verified the weekly chart renders correctly.
- Verified the monthly chart renders correctly.
- Verified the dashboard works with a copy of the existing production SQLite database.
- Verified the dashboard can be loaded through LAN with the WAN uplink physically disconnected.
- Verified Chart.js is loaded from the local application assets rather than an external CDN.


### Documentation

- Updated the README with the Alpha 3 Chart.js architecture and offline behavior.
- Marked `v2.0.0-alpha.3` as completed in the Version 2 roadmap.
- Added the final Docker packaging task for automatic extraction of the bundled Ookla Speedtest CLI archive before the Version 2 stable release.


## [v2.0.0-alpha.2] - 2026-08-20

Second functional development milestone toward Version 2.


### Added

- Added `/config` as the persistent application-state volume.
- Added `/config/settings.yaml` with default scheduler settings.
- Added automatic creation of the persistent `/config` directory structure.
- Added automatic creation of the SQLite database using the current Version 1-compatible schema when missing.
- Added scheduler configuration for clock-aligned execution intervals.
- Added scheduler timezone configuration using IANA timezone names.
- Added startup validation for scheduler settings.
- Added user-friendly configuration errors for invalid intervals, invalid types, malformed YAML, and invalid timezones.
- Added `app/config/` and `app/database/` modules.
- Added `/config/logs/` as a reserved location for future collector logging.


### Changed

- Moved persistent SQLite storage to `/config/data/speedtest.sqlite3`.
- Changed the PHP backend and collector to use the same SQLite database under `/config`.
- Changed scheduler interval and timezone values from hard-coded values to persistent settings.
- Changed collector startup to initialize persistent state before starting APScheduler.
- Moved the bundled Ookla Speedtest CLI executable to `/app/bin/speedtest`.
- Reorganized the collector image filesystem to separate collector, configuration, database, and executable files.
- Added timezone data to the collector image for configurable IANA timezone support.
- Added PyYAML as the YAML settings parser.
- Existing user-provided settings and SQLite data are preserved across container restarts and recreation.


### Validation

- Verified clean startup creates the expected `/config` structure, default settings, and SQLite database.
- Verified restarts preserve existing settings and database files.
- Verified a copy of an existing Version 1 database remains readable by the current dashboard.
- Verified supported custom intervals are applied after collector restart.
- Verified invalid scheduler intervals prevent startup with a clear configuration error.
- Verified invalid interval types and malformed YAML produce user-friendly configuration errors.


### Documentation

- Updated the README with the Alpha 2 persistent configuration behavior and settings reference.
- Marked `v2.0.0-alpha.2` as completed in the Version 2 roadmap.


## [v2.0.0-alpha.1] - 2026-08-20

First functional development milestone toward Version 2.


### Added

- Added APScheduler as the internal Speedtest scheduler.
- Added clock-aligned scheduling at HH:00, HH:15, HH:30 and HH:45.
- Added a file-based execution lock to prevent overlapping Speedtest runs.
- Added Version 2 roadmap and development documentation.


### Changed

- Changed the Speedtest collector from an ephemeral container to a persistent Docker service.
- Moved the collector source into `app/collector/`.
- Added the collector to the development Docker Compose stack.
- Configured the collector to run as an unbuffered Python process for immediate Docker log output.
- Made scheduler timezone handling explicit for the current development milestone.
- Preserved the Version 1 SQLite schema and existing PHP/Nginx dashboard behavior.


### Fixed

- Corrected the SQLite INSERT placeholder generation so collected measurements continue to be stored correctly with the existing Version 1 schema.
- Updated Ookla Speedtest CLI invocation so license/GDPR acceptance is handled when the collector runs.


### Removed

- Removed the requirement for host-based `crontab` scheduling.


### Documentation

- Added the Version 2 development roadmap.
- Added the initial Version 2 README structure.
- Documented the `v2.0.0-alpha.1` architecture milestone.


## [v1.0.0] - 2026-08-19

Initial stable release of `speed_test`.


### Added

- Dockerized Internet connection performance monitoring.
- Ookla Speedtest CLI integration.
- Persistent SQLite historical storage.
- Download and upload speed monitoring.
- Ping and loaded latency monitoring.
- 24-hour, weekly, and monthly historical views.
- PHP-based data backend.
- Nginx web server.
- Google Charts dashboard.
- Host `crontab` scheduling for automatic Speedtest execution.
- Pre-built Version 1 Docker images.
- MIT License.
