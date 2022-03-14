FROM ubuntu:18.04

RUN apt-get update
RUN apt-get install -y software-properties-common
RUN add-apt-repository -y ppa:deadsnakes/ppa

RUN apt-get update
RUN apt install -y python3.6
RUN apt install -y python3-pip
RUN apt install -y python3.6-dev libpq-dev

RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
RUN update-alternatives --config python3

RUN apt-get install -y net-tools
RUN apt-get install -y dnsutils
RUN apt-get update

ENV PYTHONUNBUFFERED 1
COPY . /home/butfit

WORKDIR /home/butfit

COPY . .
# COPY requirements.txt /home/butfit
# RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

ADD https://raw.githubusercontent.com/vishnubob/wait-for-it/master/wait-for-it.sh /