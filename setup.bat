@echo off

:RETRY
cd src

cmd /C docker login -u unimelbproject2023 -p 20232023di quay.io

docker-compose up -d

echo progressing

timeout /T 60

docker exec ontoserver /index.sh


echo Set up Succeeded

start http://localhost:3000/login

pause 