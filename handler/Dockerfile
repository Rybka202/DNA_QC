FROM python:3.11

RUN mkdir /handler_app

WORKDIR /handler_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x docker/*.sh
