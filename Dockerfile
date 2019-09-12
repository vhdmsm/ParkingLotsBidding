FROM python:3.6

ENV PYTHONUNBUFFERED 1
ENV C_FORCE_ROOT true
RUN mkdir /src
RUN mkdir /static
COPY ./parking/requirements.txt /src
RUN pip install -r /src/requirements.txt
WORKDIR /src
COPY ./parking /src