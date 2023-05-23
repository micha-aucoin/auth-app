FROM python:3.10-slim-buster as builder

WORKDIR /auth-app

COPY requirements.txt /auth-app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /auth-app/requirements.txt

COPY . /auth-app

FROM builder as dev-env

RUN <<EOF
apt-get update
apt-get install -y --no-install-recommends git
EOF




