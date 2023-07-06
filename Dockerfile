FROM python:3.10.6-slim

WORKDIR /api

COPY ./requirements.txt /api/requirements.txt

RUN pip3 install -r requirements.txt

COPY ./app /api/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]