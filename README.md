# Speed test.

(multi-container) Dockerized application for monitoring internet speed connection at home continuously.


## Getting started.

### 1. Pre-requisites.

1. To have docker installed.
2. To have this repository cloned.


### 2. Setting up the environment.

#### 1. Extract the executable "speedtest" file from the compressed API release file for the speedtest tool located at the apis folder.

```
SPEED_TEST
|-- apis
|   |-- ookla-speedtest-1.2.0-linux-x86_64.tgz
|   |-- speedtest
```


#### 2. (OPTIONAL) For creating a "speedtest only" Docker utility container, open a terminal/console and from the root path of this repository run:

```bash
# Create a "speedtest only" Docker container.
docker build -f ./Dockerfiles/speedtestonly.dockerfile .

# Get the speedtest version (replace the image_id with the one you got from the docker build command).
docker run --rm 28b04b47f067 --version

# Get help from the speedtest api (replace the image_id with the one you got from the docker build command).
docker run --rm 28b04b47f067 --help

# Run the speedtest (replace the image_id with the one you got from the docker build command).
docker run --rm 28b04b47f067 --format=json-pretty
```

Alternatively you can download the pre-built image from Dockerhub by doing:

```bash
# Pull the image from Dockerhub.
docker pull cristiancampuzano/speedtestonly:latest

# Get the speedtest version.
docker run --rm cristiancampuzano/speedtestonly:latest --version

# Get help from the speedtest api.
docker run --rm cristiancampuzano/speedtestonly:latest --help

# Run the speedtest.
docker run --rm cristiancampuzano/speedtestonly:latest --format=json-pretty
```


#### 3. For creating the database Docker container, copy the database file (/database/speedtest.sqlite3) to its final location in your system, open a terminal/console and from the root path of this repository run:

```bash
# Create the database Docker container.
docker build -f ./Dockerfiles/python.dockerfile .

# Run the database Docker container (replace the image_id with the one you got from the docker build command and the database path accordingly to what you have locally).
docker run -v C:/workspaces/speed_test/database:/app/database --rm 858f0142ecbc
```

Alternatively you can download the pre-built image from Dockerhub by doing:

```bash
# Pull the image from Dockerhub.
docker pull cristiancampuzano/speedtest-database:latest

# Run the database Docker container (replace the database path accordingly to what you have locally).
docker run -v /home/cristian/Documents/speed_test/database:/app/database --rm cristiancampuzano/speedtest-database:latest
```


#### 4. Insert a new record to crontab to auto-run the database container every 15 minutes.

```bash
# Editing crontab
$ crontab -e

# Add a scheduled task (this one will be executed every 15 minutes).
*/15 * * * * docker run -v /home/cristian/Documents/speed_test/database:/app/database --rm cristiancampuzano/speedtest-database:latest
```


#### 5. For creating and running the webpage Docker containers, open a terminal/console and from the root path of this repository run:

IMPORTANT: If you want to modify the webpage src, do some changes (documented as comments) within the docker-compose-dev.yaml and dockerfiles/php.dockerfile files before running the next command. Also do not forget to update the addresses where the volumes are pointing to.

  ```bash
  # Create the database Docker container.
  docker compose up -d
  ```
Alternatively you can download adn run the pre-built images from Dockerhub by doing:

IMPORTANT: Do not forget to update the addresses where the database volume is pointing to within the docker-compose.yaml file, you can also change the exposed port there.

```bash
# Pull the image from Dockerhub.
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

If this plugin is useful to you and you'd like to support its development:

[![Ko-fi](https://img.shields.io/badge/Ko--fi-Support%20the%20project-555?logo=ko-fi&logoColor=white)](https://ko-fi.com/cristiancampuzano)
[![PayPal](https://img.shields.io/badge/PayPal-Leave%20a%20tip-555?logo=paypal&logoColor=white)](https://paypal.me/cristianCanek)
