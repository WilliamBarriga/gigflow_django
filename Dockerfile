FROM python:3.10.1
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip gcc libpq-dev binutils libproj-dev gdal-bin gettext && ldconfig
WORKDIR /app

COPY requirements.txt .
RUN pip install -U pip
RUN pip install -r requirements.txt

EXPOSE 8000
COPY . .
# CMD gunicorn runer.wsgi -b 0.0.0.0:8000 --workers=5 --threads=2  --timeout=60