# Use the official Python image
FROM python:3.9-slim

WORKDIR /flask_app

COPY requirements.txt .
RUN pip3 install -r requirements.txt


COPY . /flask_app


# Command to run the Flask app
CMD ["gunicorn", "--workers", "--bind", "0.0.0.0:5000", "app:app"]
