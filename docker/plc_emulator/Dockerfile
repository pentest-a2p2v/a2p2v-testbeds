FROM python:latest

RUN apt update 

#RUN useradd -rm -d /home/python -s /bin/bash python 

#USER python

COPY plc_emulator.py /root/plc_emulator.py

WORKDIR /root

RUN python -m venv /root/venv

RUN . /root/venv/bin/activate

RUN pip install --upgrade pip

RUN pip install \
    pymodbus \
    twisted 

EXPOSE 502

CMD python plc_emulator.py
