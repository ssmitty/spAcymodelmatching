FROM ubuntu:22.04

RUN apt-get update \
  && apt-get install -y python3-pip python3-dev \
  && cd /usr/local/bin \
  && ln -s /usr/bin/python3 python \
  && pip3 install --upgrade pip


# Installing Python packages
RUN apt install -y git wget curl
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt