FROM alpine:latest

WORKDIR /app

RUN apk add python3 py3-virtualenv

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
COPY requirements.txt .

RUN ${VIRTUAL_ENV}/bin/pip install -r requirements.txt

COPY . /app
RUN chmod u+x ./monitor
ENV PATH="$PATH:/app"

EXPOSE 5000

# -u: print Python's print() on docker logs
CMD exec ${VIRTUAL_ENV}/bin/python3 -u -m fastapi run server.py --host 0.0.0.0 --port 5000