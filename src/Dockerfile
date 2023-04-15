FROM python:3.7

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 将代码复制到容器中
COPY . .

# 暴露端口
EXPOSE 5000

# 启动应用程序
CMD ["python", "main.py"]