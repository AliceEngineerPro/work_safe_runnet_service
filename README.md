# 项目部署

- 项目下载

```bash
git clone https://github.com/AliceEngineerPro/workspace_safe.git && cd workspace_safe
```

- 修改数据信息

```bash
sed -i "s/'HOST': '127.0.0.1'/'HOST': '{MySQLHost}'/g;s/'PORT': '3306'/'PORT': '{MySQLPort}'/g;s/'USER': 'root'/'USER': '{MySQLUser}'/g;s/'PASSWORD': 'root'/'PASSWORD': '{MySQLPassword}'/g;s/'NAME': 'safe'/'NAME': 'MySQLDatabaseName'/g" ./safe/settings.py
```

## docker部署

1. 构建  `docker build -t {image_name:image_tag} .`
2. 运行  `docker run -itd -p 8080:8080 --name safe {image_name:image_tag}`

```bash
# 查看日志
docker logs -f safe
```

## 说明

```bash
# 开放端口
# ...
```