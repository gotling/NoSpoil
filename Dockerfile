FROM python:3.9

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["gunicorn", "--conf", "gunicorn_conf.py", "--bind", "0.0.0.0:8000", "app:app"]