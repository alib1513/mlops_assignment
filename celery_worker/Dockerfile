FROM ultralytics/ultralytics:8.2.97-python

ENV CELERY_BROKER redis://redis:6379/0
ENV CELERY_BACKEND redis://redis:6379/0
ENV MODEL_PATH /celery_worker/models/yolov8n.pt

WORKDIR /celery_worker

# RUN pip3 install ultralytics


COPY requirements.txt .
RUN pip3 install -r requirements.txt

COPY . /celery_worker


# Command to run the Celery worker
CMD ["celery", "-A", "tasks.celery_worker", "worker", "--loglevel=info"]
