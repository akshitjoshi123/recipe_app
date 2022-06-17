FROM python:3.8-slim-buster
MAINTAINER Akshit Joshi

ENV PYTHONUNBUFFERED 1
USER root
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# RUN adduser -D user
# USER user
