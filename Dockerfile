FROM python:3.11-slim-buster
#FROM python:3.8-slim-buster

RUN apt-get update
RUN apt-get install ffmpeg libsm6 libxext6  -y

ENV APP_HOME /app

RUN mkdir -p $APP_HOME
#RUN mkdir -p $APP_HOME/.cache
#RUN mkdir -p ./.cache
RUN mkdir -p $APP_HOME/.cache/torch
RUN mkdir -p ./.cache/torch
RUN mkdir -p $APP_HOME/.local
RUN mkdir -p ./.local

USER root

RUN chmod -R 777 ./.cache/torch
RUN chmod -R 777 $APP_HOME/.cache/torch

RUN chmod -R 777 ./.local
RUN chmod -R 777 $APP_HOME/.local

WORKDIR $APP_HOME
#WORKDIR /app
#ADD . /app

EXPOSE 5000

COPY . .

RUN pip install -r requirements.txt


CMD [ "flask", "run", "--host=0.0.0.0"]