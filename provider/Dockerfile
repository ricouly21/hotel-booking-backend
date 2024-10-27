FROM python:latest

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements.txt .

RUN echo "Installing python dependencies ..." \
    && python -m pip install --upgrade pip \
    && python -m pip install -r ./requirements.txt \
    && python -m pip freeze > ./requirements.txt \
    echo "Done!"

COPY ./app /app

WORKDIR /app/main

EXPOSE 8000
