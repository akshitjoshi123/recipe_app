FROM python:3.8
MAINTAINER Akshit Joshi

ENV PYTHONUNBUFFERED 1
USER root
WORKDIR /app
COPY ./requirements.txt /requirements.txt
# RUN apk add --update --no-cache postgresql-client
# RUN apk add --update --no-cache --virtual .tmp-build-deps \
#         gcc libc-dev linux-headers postgresql-dev
# RUN python -m pip install --upgrade pip
RUN pip install -r /requirements.txt
# RUN apk del .tmp-build-deps

COPY ./app /app

# RUN adduser -D user
# USER user
