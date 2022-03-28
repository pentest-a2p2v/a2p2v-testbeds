FROM python:latest

RUN apt update 

RUN useradd -rm -d /home/python -s /bin/bash python 

USER python


COPY . /home/python/flaskhmi

WORKDIR /home/python/flaskhmi

ENV PATH="/home/python/.local/bin:$PATH"

RUN env

RUN echo "export PATH=/home/python/.local/bin:$PATH" >> /home/python/.bashrc

RUN python -m pip install --upgrade pip

RUN python -m pip install -r requirements.txt

EXPOSE 8800

CMD python -m flaskhmi
