
curl http://0.0.0.0:5000/

curl -X POST -d "key1=123" http://0.0.0.0:5000/start_task


curl -X POST -F "file=@test_images/bus.jpg" http://0.0.0.0:5000/start_task

curl http://0.0.0.0:5000/task_status/f5ead55f-8ab1-4daa-b843-fe03a7dea81e

curl http://0.0.0.0:5000/task_result/e95baee5-e718-4075-89e0-85534dc65470


curl http://0.0.0.0:5000/task_result/fe2808b8-35a0-4030-be69-ed92dae56afa


docker-compose up --build