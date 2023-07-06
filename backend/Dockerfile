FROM ubuntu:20.04

RUN apt-get update -y && \
    apt-get install -y python3.8 python3-pip python3.8-dev

COPY ./env/requirements.txt /workspace/env/requirements.txt
WORKDIR /workspace

ENV PYTHONPATH="$PYTHONPATH:/workspace"

# RUN pip3 install --upgrade pip
RUN pip3 install -r /workspace/env/requirements.txt

COPY . /workspace

CMD ["python3", "./src/main.py"]
