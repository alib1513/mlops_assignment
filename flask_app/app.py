import os, io, json, logging
from PIL import Image
from flask import Flask, jsonify, request
from celery import Celery

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

# Create FLask app
app = Flask(__name__)
app.logger.handlers[0].setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S'))
app.logger.setLevel(logging.DEBUG)

celery_worker = Celery('tasks', broker=os.environ.get('CELERY_BROKER'), backend=os.environ.get('CELERY_BACKEND'))



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/start_task', methods=['POST'])
def start_task():
    app.logger.info("Start Task Route")

    if 'file' not in request.files:
        return jsonify({'error': 'No image provided'}), 400


    file = request.files.getlist('file')[0]
    


    try:
        if file.filename == '' or not allowed_file(file.filename):
            response = {
            'error': f'No valid image provided. It should be among the allowed extensions: {ALLOWED_EXTENSIONS}',
            'filename': file.filename
            }
            app.logger.info(f"{file.filename} file was Invalid Image")
            return jsonify(response), 400
        

        # Read the image data
        image_data_bytes = file.read()
        # Attempt to open the image to check for corruption
        image_data = Image.open(io.BytesIO(image_data_bytes))
        image_data.verify()  # Verifies the image is not corrupted

        app.logger.info("Initiating a Celery Task for the Valid Image")


        task = celery_worker.send_task('tasks.run_inference', kwargs={
            "name" : file.filename,
            "image" : image_data_bytes
        })

        app.logger.info(f"Task Added with id: {task.id}")

        response = {
            'task_id': task.id,
            "image": file.filename,
            "status" : "Accepted. Goto /task_result/<task_id> route to check status"
        }
        return jsonify(response), 202
            

    except Exception as e:
        app.logger.error(f"Error while creating the task {e}")
        return jsonify({'error': str(e)}), 500



@app.route('/task_result/<task_id>', methods=['GET'])
def task_result(task_id):
    app.logger.info(f"Task Result Route for Task ID: {task_id}")
    result = celery_worker.AsyncResult(task_id)
    response = {"task_id": task_id}

    if result is None:
        return jsonify( response | { "error": "Not Found. The task ID does not exist."}), 400
    
    
    response = response | { "status": result.status}

    if result.state == 'SUCCESS':
        app.logger.info(result)
        response = response | json.loads(result.result)
    
    elif result.state == 'FAILURE':
        response['error'] = str(result.info)
    
    app.logger.info(f"Response for Task ID: {task_id}\n{response}")
    return jsonify(response)


@app.route('/')
def main():
    app.logger.info("Home Route")
    response = {
    "api_version": "1.0",
    "description": "Welcome to the Object Detection API. This API allows you to upload images for processing and check the status and result of your tasks.",
    "routes": [
        {
        "path": "/start_task",
        "method": "POST",
        "description": "Uploads an image for processing.",
        "request_body": {
            "request_example": 'curl -X POST -F "file=@test_images/example.jpg" http://0.0.0.0:5000/start_task',
            "file": {
                "filename": "example.jpg",
                "filetype": "image can be jpeg/jpg/png",
                "content": "<binary content of the image>",            
                "required": "true"
            }
        },
        "responses": {
            "202": {
            "description": "Accepted. The task is being processed.",
            "example":{
                "task_id": "f94c7d98-80c4-4e5d-b543-a6fa2ca332b3",
                "image": "example.jpg",
                "status" : "Accepted. Goto /task_result/<task_id> route to check status"
                }
                
            },
            "400": {
            "description": "Bad Request. Indicates a missing file or invalid input."
            }
        }
        },
        {
        "path": "/task_result/<task_id>",
        "method": "GET",
        "description": "Retrieves the status or result of a previously submitted image processing task.",
        "path_parameters": {
            "task_id": {
            "type": "string",
            "description": "The unique identifier for the task."
            }
        },
        "responses": {
            "200": {
            "description": "Success. Returns the result of the task.",
            "example_success": {
                "image_name": "bus.jpg",
                "result": [
                    {
                    "box": {
                        "x1": 22.87127,
                        "x2": 805.00262,
                        "y1": 231.27731,
                        "y2": 756.84045
                    },
                    "class": 5,
                    "confidence": 0.87345,
                    "name": "bus"
                    },
                    {
                    "box": {
                        "x1": 48.55046,
                        "x2": 245.3456,
                        "y1": 398.55231,
                        "y2": 902.7027
                    },
                    "class": 0,
                    "confidence": 0.86569,
                    "name": "person"
                    },
                    {
                    "box": {
                        "x1": 669.4729,
                        "x2": 809.72015,
                        "y1": 392.18594,
                        "y2": 877.03546
                    },
                    "class": 0,
                    "confidence": 0.85284,
                    "name": "person"
                    },
                    {
                    "box": {
                        "x1": 221.51729,
                        "x2": 344.97061,
                        "y1": 405.79865,
                        "y2": 857.53662
                    },
                    "class": 0,
                    "confidence": 0.82522,
                    "name": "person"
                    },
                    {
                    "box": {
                        "x1": 0.0,
                        "x2": 63.00691,
                        "y1": 550.52502,
                        "y2": 873.44293
                    },
                    "class": 0,
                    "confidence": 0.26111,
                    "name": "person"
                    },
                    {
                    "box": {
                        "x1": 0.05816,
                        "x2": 32.55741,
                        "y1": 254.4594,
                        "y2": 324.87415
                    },
                    "class": 11,
                    "confidence": 0.25507,
                    "name": "stop sign"
                    }
                ],
                "status": "SUCCESS",
                "task_id": "f94c7d98-80c4-4e5d-b543-a6fa2ca332b3"
                }
            },
            "example_status": {
                "status": "PENDING",
                "task_id": "f94c7d98-80c4-4e5d-b543-a6fa2ca332b3"
            },
            "400": {
            "description": "Not Found. The task ID does not exist."
            }
        }
        }
    ]
    }

    return jsonify(response)


if __name__ == '__main__':
    # Get HOST and PORT from environment variables
    host = os.getenv('FLASK_RUN_HOST', '0.0.0.0')  # Default to 0.0.0.0
    port = int(os.getenv('FLASK_RUN_PORT', 5000))     # Default to port 5000
    
    app.run(host=host, port=port)