FROM alpine

WORKDIR /app/

COPY ./requirements.txt /app/
RUN apk add python3
RUN apk add py3-pip
RUN python3 -m venv venv
RUN source venv/bin/activate && pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["venv/bin/gunicorn", "-c", "gunicorn_config.py", "server:app"]

