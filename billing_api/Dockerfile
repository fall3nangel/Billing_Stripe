FROM python:3.10.8

WORKDIR /opt/app
ENV PATH="/opt/app:${PATH}"

RUN apt-get update \
    && apt-get -y install netcat \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*


COPY requirements.txt requirements.txt


RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir


COPY . .

EXPOSE 8000

CMD ["init.sh"]