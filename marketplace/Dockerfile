# Dockerfile

FROM python:3.9
WORKDIR /
RUN python -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
ADD marketplace /marketplace/