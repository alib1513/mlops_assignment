# Use the official Python image
FROM python:3.9-slim


ENV CELERY_BROKER redis://redis:6379/0
ENV CELERY_BACKEND redis://redis:6379/0

WORKDIR /flask_app

COPY requirements.txt .
RUN pip3 install -r requirements.txt


COPY . /flask_app



# Command to run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
