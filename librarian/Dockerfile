FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -yy git && mkdir -p /app

ADD requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

WORKDIR /workspace/librarian
RUN useradd -d /home/librarian -m -u 1000 -s /bin/bash librarian

ENTRYPOINT [ "python", "-m", "app" ]
