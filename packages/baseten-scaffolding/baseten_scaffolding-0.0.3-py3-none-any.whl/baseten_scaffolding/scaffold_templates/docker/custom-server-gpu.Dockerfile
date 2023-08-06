FROM nvidia/cuda:11.3.0-cudnn8-devel-ubuntu18.04

# TF needs libcusolver.so.10 (though 11 works)
RUN ln -s /usr/local/cuda/lib64/libcusolver.so.11 /usr/local/cuda/lib64/libcusolver.so.10
ENV LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/cuda/lib64

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

RUN apt update && \
    apt install -y bash \
                   build-essential \
                   git \
                   curl \
                   ca-certificates \
                   libsndfile1 \
                   software-properties-common && \
    add-apt-repository -y ppa:deadsnakes/ppa && \
    apt update -y && \
    apt install -y python3.7 && \
    rm -rf /var/lib/apt/lists

RUN ln -sf /usr/bin/python3.7 /usr/bin/python3 && \
    curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py && \
    python3 get-pip.py

RUN python3 -m pip install --no-cache-dir --upgrade pip

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

CMD exec python3 inference_server.py
