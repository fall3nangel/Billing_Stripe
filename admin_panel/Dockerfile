FROM python:3.10.8

WORKDIR /opt/app

RUN apt update \
    && apt install -y gettext \
    && apt autoclean

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV UWSGI_PROCESSES 1
ENV UWSGI_THREADS 16
ENV UWSGI_HARAKIRI 240
ENV DJANGO_SETTINGS_MODULE 'config.settings'

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x *.sh

EXPOSE 8000

ENTRYPOINT ["./init.sh"]
