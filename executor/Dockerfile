FROM ubuntu:20.04

RUN mkdir /exec_app

WORKDIR /exec_app

COPY requirements.txt .

RUN apt-get update && \
  apt-get upgrade -y && \
  apt-get install -q -y openjdk-8-jdk python3-pip

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh

