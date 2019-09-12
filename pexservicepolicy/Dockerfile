FROM python:3.7-alpine

COPY . /web
WORKDIR /web
RUN python -m pip install --upgrade pip
RUN \
  apk update && apk add postgresql-dev gcc python3-dev musl-dev && pip install -r /web/requirements.txt

