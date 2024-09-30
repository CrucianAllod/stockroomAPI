FROM python:3.12

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker /app/docker
RUN chmod a+x docker/*.sh

COPY alembic.ini .
COPY .env-non-dev .
COPY ./src /app/src

ENV PYTHONPATH=/app/src

EXPOSE 8000
