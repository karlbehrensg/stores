FROM python:3.10-alpine

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apk update \
    && apk add python3 postgresql-libs \
    && apk add --update --no-cache --virtual .build-deps alpine-sdk python3-dev musl-dev postgresql-dev libffi-dev \
    && pip install -U setuptools pip \
    && pip install --no-cache-dir --upgrade -r /app/requirements.txt \
    && rm /app/requirements.txt \
    && apk --purge del .build-deps

COPY . /app/.

CMD ["uvicorn", "src.entrypoints.main:app", "--host", "0.0.0.0", "--port", "80"]