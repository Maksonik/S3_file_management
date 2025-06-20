ARG PLATFORM=linux/amd64
ARG PYTHON_IMAGE=python
FROM --platform=$PLATFORM $PYTHON_IMAGE:3.12-alpine AS intermediate

RUN addgroup -S app && adduser -s /bin/bash -SG app app

RUN true \
    && apk --no-cache add \
            # cryptography -> cffi
            gcc \
            musl-dev \
            libffi-dev \
            # requested by Ops
            bash \
            nano \
            vim \
            curl \
    && true

ARG PIP_INDEX_URL
ENV PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.1.3 \
    PIP_INDEX_URL=$PIP_INDEX_URL

RUN true \
    && python3 -m venv /venv \
    && . /venv/bin/activate \
    && python3 -m pip install --no-cache-dir -U pip \
    && python3 -m pip install --no-cache-dir -U poetry==$POETRY_VERSION poetry-plugin-export

ENV PATH=/venv/bin:$PATH \
    VIRTUAL_ENV=/venv

COPY pyproject.toml poetry.lock /tmp/

RUN cd /tmp \
    && poetry export --only=main --without-urls --format requirements.txt --output requirements.txt \
    && rm pyproject.toml poetry.lock \
    && python3 -m pip install --no-cache-dir -U -r requirements.txt \
    && rm requirements.txt


FROM intermediate AS testing

RUN apk --no-cache add \
      git

RUN git config --global safe.directory '*'

COPY pyproject.toml poetry.lock /tmp/

RUN cd /tmp \
    && poetry export --only=dev --without-urls --format requirements.txt --output requirements.txt \
    && rm pyproject.toml poetry.lock \
    && python3 -m pip install --no-cache-dir -U -r requirements.txt \
    && rm requirements.txt


FROM intermediate AS release

ENV CODE_DIR=/code

COPY .. $CODE_DIR/

USER app
WORKDIR $CODE_DIR
