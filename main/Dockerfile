FROM python:3.9

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2-binary

RUN pip install --upgrade pip
WORKDIR . /main
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .