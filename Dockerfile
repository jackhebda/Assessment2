FROM python:3.8-alpine

WORKDIR /app
ADD . /app/

RUN /sbin/apk add --virtual .deps gcc musl-dev\
 && /usr/local/bin/pip install --no-cache-dir black==19.10b0 \
 && /sbin/apk del .deps

RUN apk add build-base

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000
