FROM python:3.9.16-slim

WORKDIR /playwright-app

COPY requirements.txt .
RUN pip install -r requirements.txt









RUN apt-get update && apt-get install git \
    && apt-get default-jdk


RUN playwright install


ENTRYPOINT ["tail","-f", "/dev/null"]
