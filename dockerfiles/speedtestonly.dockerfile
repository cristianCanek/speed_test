FROM alpine:3.22.0

WORKDIR /app

COPY ./apis/speedtest .

RUN /app/speedtest --accept-license

ENTRYPOINT ["/app/speedtest"]