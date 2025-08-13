FROM python:3.10.13-slim
LABEL maintainer="Ilgiz Rakhimianov <i@rakhimianov.ru>"

ARG DEPENDENCIES="vim nano locales tzdata"
RUN apt-get update && apt-get install -y $DEPENDENCIES

RUN sed -i '/ru_RU.UTF-8/s/^# //g' /etc/locale.gen && locale-gen
ENV LANG ru_RU:ru
ENV LANGUAGE ru_Ru:ru
ENV LC_ALL ru_RU.UTF-8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /opt/app

COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD python main.py