FROM python:latest

EXPOSE 8000

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

RUN apt-get update \
    && DEBIAN_FRONTEND=noninteractive \
    apt-get install --no-install-recommends --assume-yes \
    postgresql \
    libpq-dev
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
COPY requirements.txt .
RUN python -m pip install -r requirements.txt
COPY . .
