FROM python:3.10.13-slim

ARG DEPENDENCIES="vim nano tzdata"
RUN apt update && apt install -y $DEPENDENCIES

WORKDIR /opt/app/bot

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["python", "main.py"]