FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y gcc build-essential libpq-dev default-libmysqlclient-dev openjdk-17-jre-headless pkg-config && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt 

RUN pip install --no-cache-dir gunicorn

COPY . .

RUN python manage.py collectstatic --noinput || true

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=dl4ml.settings

CMD ["gunicorn", "dl4ml.wsgi:application", "--bind", "0.0.0.0:8000"]
