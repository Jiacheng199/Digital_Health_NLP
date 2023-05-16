cd src
docker login -u unimelbproject2023 -p 20232023di quay.io
docker-compose up -d
docker exec ontoserver /index.sh
pause