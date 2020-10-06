FROM python:3.8.6-alpine
ENV PYTHONDOTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
WORKDIR /usr/src/app
COPY . .
RUN apk update && apk add --no-cache gcc libc-dev make libffi-dev python3-dev libxml2-dev libxslt-dev postgresql-dev jpeg-dev zlib-dev && pip install -r requirements.txt
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
