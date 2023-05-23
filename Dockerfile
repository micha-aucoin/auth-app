FROM python:3.10-slim-buster as builder

WORKDIR /auth-app

COPY requirements.txt /auth-app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /auth-app/requirements.txt

COPY . /auth-app

FROM pychal/ku-toolz:latest as dev-env

COPY --from=builder /auth-app /auth-app
COPY --from=builder /usr/local/bin/ /usr/local/bin/
COPY --from=builder /usr/local/lib/python3.10/ /usr/local/lib/python3.10/



