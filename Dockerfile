#FROM python:3.4-alpine
FROM ubuntu:latest
MAINTAINER Rajdeep Dua "dua_rajdeep@yahoo.com"
RUN apt-get update -y
RUN apt-get install -y python-pip python-dev build-essential
RUN apt-get -y install python-mysql.connector
#RUN apt-get -y install mysql-client
#RUN apt-get -y install iputils-ping
ADD . /app
WORKDIR /app
RUN pip install -r requirements.txt
CMD ["python", "app.py"]