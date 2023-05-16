@echo off

:RETRY
REM 进入 src 目录
cd src

REM 登录到 Docker
cmd /C docker login -u unimelbproject2023 -p 20232023di quay.io


REM 使用 docker-compose 启动容器
docker-compose up -d


REM 在 "ontoserver" 容器中执行 index.sh 脚本
docker exec ontoserver /index.sh

echo Set up Succeeded

REM 打开网页 https://localhost:3000
start http://localhost:3000/login

REM 退出批处理脚本
pause