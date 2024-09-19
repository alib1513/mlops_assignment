import os, io, json
from PIL import Image
from celery import Celery
from celery.utils.log import get_task_logger
from ultralytics import YOLO


logger = get_task_logger(__name__)


CELERY_BROKER = os.environ.get('CELERY_BROKER')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND')
MODEL_PATH = os.environ.get('MODEL_PATH')

celery_worker =  Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)
celery_worker.conf.broker_connection_retry_on_startup = True






class YoloModel:
    def __init__(self, model_name="yolov8n.pt", conf = 0.3):
        self.model = YOLO(model_name)
        self.model.conf = conf

    def detect_objects(self, image):
        results = self.model(image)

        return json.loads(results[0].to_json())[0]



yolo_model = YoloModel(model_name=MODEL_PATH)




@celery_worker.task(name='tasks.run_inference', trail=True)
def run_inference(name, image):
    logger.info('Got Request - Starting Inference')

    # Save the image

    # give the path to the worker

    # image_data = json.loads(image_data)

    # names = image_data["names"]
    # images = image_data["images"]

    # time.sleep(3)
    result = yolo_model.detect_objects(Image.open(io.BytesIO(image)))

    logger.info('Inference Finished')




    return json.dumps({"name":name, "result": result})