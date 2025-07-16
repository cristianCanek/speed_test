FROM python:3.13.5-alpine3.22

WORKDIR /app

COPY ./apis/speedtest .

RUN /app/speedtest --accept-license

COPY ./src/speedtest.py .

CMD ["python", "/app/speedtest.py"]