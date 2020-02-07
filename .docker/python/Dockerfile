FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7

RUN apk update \
    && apk add gcc musl-dev \
    && apk add postgresql-dev python3-dev

ENV STATIC_URL /static
ENV STATIC_PATH /app/frontend/dist/static

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
