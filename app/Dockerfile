FROM python:3.6-alpine3.8

ENV PYTHONUNBUFFERED 1
ENV LIBRARY_PATH=/lib:/usr/lib
ENV LANG en_US.UTF-8

RUN apk update \
    && apk add --update-cache --virtual build-deps build-base \
        musl-dev \
        git \
        postgresql-dev \
        jpeg-dev \
        zlib-dev \
        libffi-dev \
    \
    && apk add --update-cache \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/testing/ \
        --repository http://dl-cdn.alpinelinux.org/alpine/edge/main/ \
        --allow-untrusted \
        gdal-dev \
        geos-dev \
    \
    && rm -rf /var/cache/apk/* \
    \
    && mkdir -p /opt/semantive/requirements

WORKDIR /opt/semantive
ADD requirements /opt/semantive/requirements/
ADD requirements /opt/semantive/requirements/

RUN pip install -U setuptools \
    \
    && pip install -r /opt/semantive/requirements/dev.pip

RUN mkdir -p /data/imgs

#ADD entrypoint.sh .
#RUN chmod +x ./entrypoint.sh
#CMD /./entrypoint.sh
# CMD /opt/semantive/entrypoint.sh
# CMD "/usr/local/bin/python3.6 manage.py runserver"

# EXPOSE 8000
