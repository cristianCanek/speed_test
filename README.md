# Speed test.

Self-hosted multi-container Docker application for continuously monitoring Internet connection performance using Ookla Speedtest CLI, SQLite, and a local web dashboard.

| | |
|---|---|
| ![Latest result](docs/images/dashboard_01.png) | ![24-hour dashboard](docs/images/dashboard_02.png) |
| ![Weekly dashboard](docs/images/dashboard_03.png) | ![Monthly dashboard](docs/images/dashboard_04.png) |


## Architecture

Version 1.x uses a multi-container architecture composed of separate components for data collection and web visualization.

```text
                         Host system
                             │
                             │ crontab (every 15 minutes)
                             ▼
                ┌─────────────────────────┐
                │ Speedtest database      │
                │ container               │
                │                         │
                │ Python                  │
                │ Ookla Speedtest CLI     │
                └────────────┬────────────┘
                             │
                             │ writes results
                             ▼
                   ┌───────────────────┐
                   │ SQLite database   │
                   │ speedtest.sqlite3 │
                   └─────────┬─────────┘
                             │
                       bind-mounted
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     ┌─────────────────┐          ┌─────────────────┐
     │ PHP container   │◄─────────│ Nginx container │
     │                 │          │                 │
     │ Reads SQLite    │          │ Serves web UI   │
     │ Generates data  │          │ Port 8000       │
     └─────────────────┘          └────────┬────────┘
                                          │
                                          ▼
                                       Browser
                                          │
                                          ▼
                                  Google Charts
```

### Components

**Speedtest collector**

A Python-based Docker container executes the Ookla Speedtest CLI, parses its JSON output, and stores the resulting measurements in a SQLite database.

The container is designed to run as an ephemeral container. In the default setup, the host system invokes it every 15 minutes using `crontab`.

**SQLite database**

Speed test results are stored persistently in a SQLite database located outside the container through a bind mount. This allows the collected historical data to survive container recreation and updates.

**PHP backend**

The PHP container reads historical measurements from the SQLite database and prepares the data used by the web interface.

**Nginx web server**

Nginx serves the web application and forwards PHP requests to the PHP container. By default, the dashboard is available on port `8000`.

**Web dashboard**

The browser displays the collected results using Google Charts. Version 1.x therefore requires Internet access to load the Google Charts library even though the application itself is hosted locally.

### Data flow

```text
Ookla Speedtest CLI
        │
        ▼
     Python
        │
        ▼
     SQLite
        │
        ▼
       PHP
        │
        ▼
      Nginx
        │
        ▼
Web browser / Google Charts
```

### Version 1.x limitations

Version 1.x is fully functional, but its original architecture has several limitations that motivated the Version 2 refactor:

* Multiple containers are required for a relatively small application.
* Speed tests are scheduled by the host system using `crontab`.
* Initial database setup requires manual steps.
* Configuration such as the execution interval is not centralized.
* The web frontend depends on Google Charts and therefore requires Internet access to load the charting library.
* PHP directly prepares data for JavaScript visualization, tightly coupling data access and presentation.
* There is no public REST API for external integrations.
* Failed speed tests are not represented as first-class monitoring events.
* The dashboard has limited responsive behavior.
* Installation requires several manual configuration steps and host-specific paths.

Version 2 is intended to preserve the core functionality of Version 1 while simplifying deployment, improving portability, removing external frontend dependencies, and exposing a cleaner interface for future integrations.


## Getting started.

### 1. Pre-requisites.

1. To have docker installed.
2. To have this repository cloned.


### 2. Setting up the environment.

#### 1. Extract the executable "speedtest" file from the compressed CLI release file for the speedtest tool located at the apis folder.

```
SPEED_TEST
|-- apis
|   |-- ookla-speedtest-1.2.0-linux-x86_64.tgz
|   |-- speedtest
```


#### 2. (OPTIONAL) For creating a "speedtest only" Docker utility container, open a terminal/console and from the root path of this repository run:

```bash
# Create a "speedtest only" Docker container.
docker build -f ./dockerfiles/speedtestonly.dockerfile .

# Get the speedtest version (replace the image_id with the one you got from the docker build command).
docker run --rm 28b04b47f067 --version

# Get help from the speedtest CLI (replace the image_id with the one you got from the docker build command).
docker run --rm 28b04b47f067 --help

# Run the speedtest (replace the image_id with the one you got from the docker build command).
docker run --rm 28b04b47f067 --format=json-pretty
```

Alternatively you can download the pre-built image from Docker Hub by doing:

```bash
# Pull the image from Docker Hub.
docker pull cristiancampuzano/speedtestonly:1.0.0

# Get the speedtest version.
docker run --rm cristiancampuzano/speedtestonly:1.0.0 --version

# Get help from the speedtest CLI.
docker run --rm cristiancampuzano/speedtestonly:1.0.0 --help

# Run the speedtest.
docker run --rm cristiancampuzano/speedtestonly:1.0.0 --format=json-pretty
```


#### 3. For creating the database Docker container, copy the database file (/database/speedtest.sqlite3) to its final location in your system, open a terminal/console and from the root path of this repository run:

```bash
# Create the database Docker container.
docker build -f ./dockerfiles/python.dockerfile .

# Run the database Docker container (replace the image_id with the one you got from the docker build command and the database path accordingly to what you have locally).
docker run -v C:/workspaces/speed_test/database:/app/database --rm 858f0142ecbc
```

Alternatively you can download the pre-built image from Docker Hub by doing:

```bash
# Pull the image from Docker Hub.
docker pull cristiancampuzano/speedtest-database:1.0.0

# Run the database Docker container (replace the database path accordingly to what you have locally).
docker run -v /home/cristian/Documents/speed_test/database:/app/database --rm cristiancampuzano/speedtest-database:1.0.0
```


#### 4. Insert a new record to crontab to auto-run the database container every 15 minutes.

```bash
# Editing crontab
$ crontab -e

# Add a scheduled task (this one will be executed every 15 minutes).
*/15 * * * * docker run -v /home/cristian/Documents/speed_test/database:/app/database --rm cristiancampuzano/speedtest-database:1.0.0
```


#### 5. For creating and running the webpage Docker containers, open a terminal/console and from the root path of this repository run:

IMPORTANT: If you want to modify the webpage src, do some changes (documented as comments) within the docker-compose-dev.yaml and dockerfiles/php.dockerfile files before running the next command. Also do not forget to update the addresses where the volumes are pointing to.

  ```bash
  # Up the web Docker containers.
  docker compose up -d
  ```
Alternatively you can download and run the pre-built images from Docker Hub by doing:

IMPORTANT: Do not forget to update the addresses where the database volume is pointing to within the docker-compose.yaml file, you can also change the exposed port there.

```bash
# Pull the image from Docker Hub.
docker compose -f docker-compose.yaml up -d
```


### 3. Monitor the results using a web page.

Once you have the webpage docker containers running, open your browser and go to [http://localhost:8000/](http://localhost:8000/) to watch the results. Change the port or ip address based on your setup.


## License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for details.


## Third-party software

This project uses Ookla's Speedtest CLI to perform network speed measurements.
Ookla Speedtest CLI is distributed and licensed separately by Ookla.


## Disclaimer

This project is provided for personal monitoring and informational purposes. Speed test results may vary depending on network conditions, test server selection, hardware, ISP behavior, and other factors. Results should not be considered a guaranteed measurement of service quality or availability.

This project is not affiliated with, endorsed by, or sponsored by Ookla. Speedtest® and Ookla® are trademarks of Ookla, LLC.


## Support

If this project is useful to you and you'd like to support its development:

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20the%20project-555?logo=ko-fi&logoColor=white)](https://ko-fi.com/cristiancampuzano)
[![PayPal](https://img.shields.io/badge/PayPal-Leave%20a%20tip-555?logo=paypal&logoColor=white)](https://paypal.me/cristianCanek)
