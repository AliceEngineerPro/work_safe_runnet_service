FROM python:3.7
WORKDIR /app
COPY . /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
EXPOSE 8080
CMD ["python", "manage.py", "run", "server", "0.0.0.0:8080"]