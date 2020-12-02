FROM python:3.8-alpine

WORKDIR /app
ADD . /app/

RUN /sbin/apk add --no-cache --virtual .deps gcc musl-dev \
 && /usr/local/bin/pip install --no-cache-dir black==19.10b0 \
 && /sbin/apk del --no-cache .deps

RUN apk add --no-cache build-base

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

RUN python -m uvicorn app:app --reload --log-config logger.conf --log-level debug --port 5000
