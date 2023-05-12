FROM python:3.8-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN pip3 install xmltodict

COPY . .

ENV AMBIENTEPROXY=www.ping.com.br

CMD [ "python3", "microserviceCalc.py", "run", "--host=0.0.0.0"]
