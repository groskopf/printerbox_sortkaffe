FROM ghcr.io/groskopf/printerbox_python


COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /tmp/requirements.txt

RUN mkdir -p /app/src
COPY src/ /app/src


