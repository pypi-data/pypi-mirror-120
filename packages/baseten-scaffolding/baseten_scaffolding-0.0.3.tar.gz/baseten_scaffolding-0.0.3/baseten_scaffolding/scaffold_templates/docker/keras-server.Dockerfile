FROM python:3.7

ARG RUNTIME_ENV

COPY ./src/server_requirements.txt server_requirements.txt
COPY ./requirements.txt requirements.txt

RUN pip install -r server_requirements.txt
RUN pip install -r requirements.txt

ENV PORT 8080
ENV RUNTIME_ENV=$RUNTIME_ENV

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY ./src .

CMD exec python inference_server.py
