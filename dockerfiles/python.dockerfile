FROM python:3.13.5-alpine3.22

WORKDIR /app

RUN apk add --no-cache tzdata

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app/logging_config.py ./logging_config.py
COPY ./app/collector         ./collector
COPY ./app/config            ./config
COPY ./app/database          ./database

RUN mkdir -p /app/bin
COPY ./apis/speedtest /app/bin/speedtest
RUN chmod +x /app/bin/speedtest

STOPSIGNAL SIGINT

CMD ["python", "-u", "-m", "collector", "scheduler"]
