
curl http://0.0.0.0:5000/

curl -X POST -d "key1=123" http://0.0.0.0:5000/start_task


curl -X POST -F "file=@test_images/bus.jpg" http://0.0.0.0:5000/start_task

curl http://0.0.0.0:5000/task_status/e06cf74b-f08e-40e9-9fb4-85171cd98c4d

curl http://0.0.0.0:5000/task_result/af6bc5ff-52c1-489f-80b6-cbcb0d0943e8


curl http://0.0.0.0:5000/task_result/fe2808b8-35a0-4030-be69-ed92dae56afa


docker-compose up --build