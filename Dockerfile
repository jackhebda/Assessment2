FROM python:3.8-alpine

WORKDIR /exam
ADD . /exam/

RUN /sbin/apk add --virtual .deps gcc musl-dev\
 && /usr/local/bin/pip install black\
 && /sbin/apk del .deps

RUN apk add build-base

RUN pip install -r requirements.txt

EXPOSE 5000
