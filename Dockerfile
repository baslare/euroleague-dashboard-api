FROM python:3.10.6-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip3 install -r requirements.txt
