FROM python:3.10

WORKDIR /app/

COPY ./requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

EXPOSE 5000

CMD ["gunicorn", "-c", "gunicorn_config.py", "server:app"]

