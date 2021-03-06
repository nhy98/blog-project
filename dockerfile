FROM python:3.8
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8

RUN apt-get update && apt-get -y install python3-pip

RUN unlink /etc/localtime && ln -s /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime
COPY ./timezone /etc/timezone

RUN pip3 install --upgrade pip

COPY ./requirements.txt /

RUN pip3 install -r /requirements.txt
ADD / /
ENTRYPOINT cd /src && python3 app.py
