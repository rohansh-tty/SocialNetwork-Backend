FROM python:3.10

ENV PYTHONUNBUFFERED 1 
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

COPY . /app/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn


RUN python manage.py collectstatic --noinput

CMD ["gunicorn", "--bind", "0.0.0.0:8010", "social_network.wsgi:application"]

