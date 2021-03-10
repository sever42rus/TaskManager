FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /backend

COPY ./backend/requirements.txt /backend/requirements.txt
RUN pip install -r /backend/requirements.txt



