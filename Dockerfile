FROM python:3.8-slim-buster

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./Model ./Model

COPY ./src ./src

CMD [ "python3", "./src/Main.py"]