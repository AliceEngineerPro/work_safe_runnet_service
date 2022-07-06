# 本地部署

1. 安装python环境  [下载地址](https://www.python.org/downloads/release/python-378/)
2. 安装依赖模块  `pip install -r requirements.txt`
3. 修改数据库配置
4. 启动程序  `python manage.py runserver`

# docker部署

1. 构建docker容器  `docker build -t .`
2. 运行  `docker run -d -p 8080:8080 --name safe --restart always `
