FROM python:3.13

RUN apt update && apt upgrade -y
RUN pip install --upgrade pip

RUN apt install -y libdbus-1-dev libdbus-glib-1-dev

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /var/www/observability/
COPY . .
RUN pip install -r requirements.txt

EXPOSE 5000