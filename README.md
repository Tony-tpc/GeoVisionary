# GeoVisionary 后端服务器
> 基于 `Django+Mysql+neo4j` 
## 部署指南

### 安装
```shell
git clone -b backend https://github.com/Tony-tpc/GeoVisionary
cd GeoVisionary
```

> [!WARNING]
> 最好使用虚拟环境
```shell
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```


### 运行
```shell
python manage.py runserver
```
> [!WARNING]
> 在./neo4jDB中的模型和视图函数无法在缺失neo4j的服务器下运行