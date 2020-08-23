# Dockerfile to create Python container

FROM python:3.7.9-slim-buster

RUN apt-get update

COPY python/requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

CMD tail -f /dev/null
