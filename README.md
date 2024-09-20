
---

# MLOps Assignment App

This project is a Flask application that leverages Redis as a message broker for Celery. It is designed with vertical scalability in mind, allowing you to optimize resource usage on a single server while handling asynchronous tasks efficiently.

## Table of Contents

- [Features](#features)
- [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Running the Application](#running-the-application)
- [Vertical Scalability](#vertical-scalability)


## Features

- Asynchronous task processing with Celery to run inference on images
- Redis as a message broker
- Flask web framework
- Easy configuration using environment variables
- Vertical scalability to optimize performance

## Technologies Used

- **Flask**: Web framework for building the application.
- **Redis**: In-memory data structure store used as a message broker.
- **Celery**: Asynchronous task queue/job queue for managing background tasks.
- **Docker**: Containerization for easy deployment and scaling.

## Getting Started

### Prerequisites

- Docker and Docker Compose.

### Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/alib1513/mlops_assignment.git
   cd mlops_assignment
   ```

2. Update the `.env` file in the project root if you want to change the HOST and PORT of flask app:

   ```env
    FLASK_RUN_HOST=0.0.0.0
    FLASK_RUN_PORT=5000
   ```



## Running the Application

To build and start the application, run:

```bash
docker-compose up --build
```
This command will start the Flask app, Redis, and Celery worker in separate containers.

### Home route list alls the paths
```bash
curl http://0.0.0.0:5000/
```

    {
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



### Upload the image and start the task on using the following the curl command

```bash
curl -X POST -F "file=@test_images/bus.jpg" http://0.0.0.0:5000/start_task
```

If the task was accepted, then the api will return the following:
    {
    "image":"bus.jpg",
    "status":"Accepted. Goto /task_result/<task_id> route to check status",
    "task_id":"3cee6d21-bdd5-4cb5-befd-34e2690b93be"
    }


### Check the task for results for a task ID using the following the curl command

```bash
curl http://0.0.0.0:5000/task_result/3cee6d21-bdd5-4cb5-befd-34e2690b93be
```

If task is still pending, then api will return the following

    {
        "status": "PENDING",
        "task_id": "f94c7d98-80c4-4e5d-b543-a6fa2ca332b3"
    }

If task is successfully completed, then api will return the following

    {
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






## Vertical Scalability

Vertical scalability allows you to optimize your application's performance on a single server by:

- **Increasing Resources**: Allocate more CPU and RAM to your containers via Docker Compose.

Resource limits can be adjusted in `docker-compose.yml`:

```yaml
services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G

  worker:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
```


- **Optimizing Celery Workers**: Adjust the concurrency settings of Celery workers if cpu cores are increased to handle more tasks simultaneously.

Number of concurrent workers for a single celery instance can be adjusted in `docker-compose.yml` by updating the concurrency tag:

```yaml
services:

  worker:
    command: [ "celery", "-A", "tasks.celery_worker", "worker", "--concurrency=4", "--loglevel=info" ]
```

- **Replicas**: Running multiple instances of the celery worker by increasing multiple replicas of Celery

```yaml
services:

  worker:
    deploy:
      replicas: 2
      resources:
        limits:
          cpus: '2'
          memory: 2G
```

- **Increasing the number of gunicorn worker**: The gunicorn allows to specify the number of worker processes that it should spawn which more to handle request concurrently. It can updated by changing the number of workers in `docker-compose.yml`

```yaml
services:

  worker:
    command: [ "gunicorn", "--workers", "4", "--bind", "0.0.0.0:5000", "app:app" ]
```

---

