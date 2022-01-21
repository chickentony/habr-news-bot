FROM python:3.7-slim-buster

RUN mkdir -p /usr/src/app/
WORKDIR /usr/src/app/

RUN apt-get update && apt-get install make

COPY . /usr/src/app/
RUN pip3 install -r requirements.txt

RUN make test
RUN make lint

CMD python3 main.py
