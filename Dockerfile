FROM python:3-slim-buster as builder

WORKDIR /auth-app

COPY requirements.txt /auth-app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /auth-app/requirements.txt

COPY . /auth-app


FROM builder as dev-env
RUN apt update && \
    apt install -y --no-install-recommends \
    git
RUN useradd -s /bin/bash -m vscode && \
    groupadd docker && \
    usermod -aG docker vscode
COPY --from=gloursdocker/docker / /
