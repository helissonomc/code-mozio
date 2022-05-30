FROM python:3.9-alpine3.13


ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /tmp/requirements.txt
COPY ./scripts /scripts
COPY ./app/ /app
WORKDIR /app
EXPOSE 8000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user && \
    mkdir -p /vol/web/media && \
    mkdir -p /vol/web/static && \
    chown -R django-user:django-user /vol && \
    chmod -R 755 /vol && \
    chmod -R +x /scripts
# It is necessary to use PostGis with django
RUN apk add --no-cache geos proj gdal
# Setup directory structure

ENV PATH="/scripts:/py/bin:$PATH"
USER django-user

CMD ["run.sh"]