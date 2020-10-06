FROM python:3.8.6-alpine
ENV PYTHONDOTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
WORKDIR /usr/src/app
RUN apk update && apk install postgresql-dev gcc python3-dev musl-dev
COPY . .
RUN pip install -r requirements.txt

