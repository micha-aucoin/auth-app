FROM python:3.10-slim-buster as builder

WORKDIR /auth-app

COPY requirements.txt /auth-app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /auth-app/requirements.txt

COPY . /auth-app

FROM ghcr.io/micha-aucoin/ku-toolz:sha-4be1fed as dev-env

COPY --from=builder /auth-app /auth-app
COPY --from=builder /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages


