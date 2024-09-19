import os, time, json
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
    def __init__(self, model_name="yolov8n.pt", conf = 0.5):
        self.model = YOLO(model_name)
        self.model.conf = conf

    def detect_objects(self, names, images):
        results = self.model(images)
        results_dict = {}
        # results_list = []
        
        for index, result in enumerate(results):
            results_dict[names[index]] = json.loads(result.to_json())[0]
            # results_list.append(json.loads(result.to_json())[0])

        return results_dict



yolo_model = YoloModel(model_name=MODEL_PATH)




@celery_worker.task(name='tasks.run_inference', trail=True)
def run_inference(image_data):
    logger.info('Got Request - Starting Inference')

    image_data = json.loads(image_data)

    names = image_data["names"]
    images = image_data["images"]

    # time.sleep(3)
    results = yolo_model.detect_objects(names, images)

    logger.info('Inference Finished')




    return json.dumps({"results":results})