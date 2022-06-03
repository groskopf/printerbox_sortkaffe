FROM printerbox_python:v2


RUN mkdir -p /app/src
COPY src/ /app/src

