FROM python:3.8.6-alpine as builder
ENV PYTHONDOTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1
WORKDIR /usr/src/app
COPY . .
RUN apk update && apk add --no-cache gcc libc-dev make libffi-dev python3-dev libxml2-dev libxslt-dev postgresql-dev jpeg-dev zlib-dev
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/app/wheels -r requirements.txt

FROM python:3.8.6-alpine
RUN mkdir -p /home/app
RUN addgroup -S app && adduser -S app -G app
ENV HOME=/home/app
ENV APP_HOME=/home/app/web
RUN mkdir $APP_HOME
WORKDIR $APP_HOME
RUN apk update && apk add libpq
COPY --from=builder /usr/src/app/wheels /wheels
COPY --from=builder /usr/src/app/requirements.txt .
RUN pip install --no-cache /wheels/*
COPY ./entrypoint.prod.sh $APP_HOME
COPY . $APP_HOME
RUN chown -R app:app $APP_HOME
USER app
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
