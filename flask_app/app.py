import os, io, json
from PIL import Image
from flask import Flask, jsonify, request

app = Flask(__name__)

CELERY_BROKER = os.environ.get('CELERY_BROKER', 'redis://redis:6379/0')
CELERY_BACKEND = os.environ.get('CELERY_BACKEND', 'redis://redis:6379/0')

from celery import Celery
celery_worker = Celery('tasks', broker=CELERY_BROKER, backend=CELERY_BACKEND)


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/start_task', methods=['POST'])
def start_task():
    app.logger.info("Inside start_task route")

    if 'file' not in request.files:
        return jsonify({'error': 'No image provided'}), 400


    files = request.files.getlist('file')
    app.logger.info(files)
    
    valid_names = []
    valid_images = []
    invalid_images = []
    
    try:
        # Iterate over the uploaded files
        for file in files:
            if file.filename == '':
                invalid_images.append({'filename': file.filename, 'error': 'No selected file'})
                continue
            
            if not allowed_file(file.filename):
                invalid_images.append({'filename': file.filename, 'error': 'Invalid Image type'})
                continue
            
            try:
                # Read the image data
                image_data_bytes = file.read()
                # Attempt to open the image to check for corruption
                image_data = Image.open(io.BytesIO(image_data_bytes))
                image_data.verify()  # Verifies the image is not corrupted

                app.logger.info(image_data)

                valid_names.append(file.filename)
                valid_images.append(image_data)

            except Exception as e:
                invalid_images.append({'filename': file.filename, 'error': str(e)})



        if len(valid_images) > 0:
            app.logger.info("Starting Celery Task for Valid Images")

            image_data = {
                "names" : valid_names,
                "images" : valid_images
            }

            task = celery_worker.send_task('tasks.run_inference', kwargs={'image_data': json.dumps(image_data)})
            app.logger.info(task.backend)

            response = {
                'task_id': task.id,
                "valid_images": valid_names,
                'invalid_images': invalid_images
            }
            return jsonify(response), 202
        else:
            response = {
                'error': 'No valid image provided',
                'invalid_images': invalid_images
            }
            return jsonify(response), 400

    except Exception as e:
        return jsonify({'error': str(e)}), 500


    


@app.route('/task_status/<task_id>', methods=['GET'])
def get_status(task_id):
    status = celery_worker.AsyncResult(task_id, app=celery_worker)
    app.logger.info("Status of Task")
    return jsonify({"task_id": task_id, "status": status.state})


@app.route('/task_result/<task_id>', methods=['GET'])
def task_result(task_id):
    result = celery_worker.AsyncResult(task_id)
    print(result)
    return jsonify({"task_id": task_id, "status": result.status, "result": result.result})


@app.route('/')
def main():
    app.logger.info("Inside Home Route")
    return jsonify({"main":"Start New Task By Going to /start_task route"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)