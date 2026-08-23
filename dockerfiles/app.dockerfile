FROM python:3.13.5-alpine3.22

WORKDIR /app

RUN apk add --no-cache tzdata

COPY ./requirements-app.txt .
RUN pip install --no-cache-dir -r requirements-app.txt

COPY ./app/main.py  .
COPY ./app/api      ./api
COPY ./app/config   ./config
COPY ./app/database ./database

COPY ./web_page ./static

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
