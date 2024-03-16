FROM alpine

WORKDIR /app/

COPY . /app/
RUN apk add python3
RUN apk add py3-pip

ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "-u", "-m", "gunicorn", "-c", "gunicorn_config.py", "server:app"]
