FROM python:3.7
ARG MODEL_CLASS
ARG MODEL_CLASS_DEFINITION_FILE

COPY ./src/server_requirements.txt server_requirements.txt
COPY ./requirements.txt requirements.txt

RUN pip install -r server_requirements.txt
RUN pip install -r requirements.txt

ENV PORT 8080

ENV APP_HOME /app
WORKDIR $APP_HOME
ENV MODEL_CLASS_NAME=$MODEL_CLASS
ENV MODEL_CLASS_FILE=$MODEL_CLASS_DEFINITION_FILE
COPY ./src .

CMD exec python inference_server.py
