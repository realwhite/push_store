FROM python:3.8-slim
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -U -r /tmp/requirements.txt
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.7.3/wait /wait
RUN chmod +x /wait
WORKDIR /code
