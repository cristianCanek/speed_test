FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apis/speedtest .

COPY ./app/collector/speedtest.py .

STOPSIGNAL SIGINT

CMD ["python", "-u", "/app/speedtest.py"]