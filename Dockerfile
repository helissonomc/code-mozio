FROM python:3.9-alpine3.13


ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
COPY ./requirements.dev.txt /requirements.dev.txt

ARG DEV=false

RUN pip install --upgrade pip  && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev && \
    if [ $DEV = "true" ]; then \
        pip install -r /requirements.dev.txt; \
    fi && \
    pip install -r /requirements.txt

RUN apk del .tmp-build-deps

# Setup directory structure
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app
EXPOSE 8000

RUN adduser -D user
USER user