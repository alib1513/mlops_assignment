FROM ultralytics/ultralytics:8.2.97-python

WORKDIR /celery_worker

COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /celery_worker


# Command to run the Celery worker
CMD ["celery", "-A", "tasks.celery_worker", "worker", "--loglevel=info"]
