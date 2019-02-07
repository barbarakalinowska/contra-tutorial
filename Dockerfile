FROM ubuntu:18.04

RUN apt-get update && apt-get install -y wget ca-certificates \
    build-essential cmake pkg-config \
    libatlas-base-dev gfortran \
    git curl python3-dev python3-pip \
    libfreetype6-dev libhdf5-dev && \
    rm -rf /var/lib/apt/lists/*


COPY /app/requirements.txt /tutorial_app/requirements.txt

RUN pip3 install  --upgrade pip
RUN pip3 install -r /tutorial_app/requirements.txt

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8