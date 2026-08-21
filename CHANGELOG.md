# Changelog

All notable changes to this project will be documented in this file.

This project follows [Semantic Versioning](https://semver.org/).

Development plans and upcoming milestones are documented separately in [ROADMAP.md](ROADMAP.md).


## Table of Contents

- [[v2.0.0-alpha.2] - 2026-08-20](#v200-alpha2---2026-08-20)
- [[v2.0.0-alpha.1] - 2026-08-20](#v200-alpha1---2026-08-20)
- [[v1.0.0] - 2026-08-19](#v100---2026-08-19)


## [Unreleased]

No unreleased changes yet.


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
