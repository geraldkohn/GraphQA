# GraphQA 

Knowledge Graph-based Question-Answering System.

## 部署

1. 安装 Python 依赖包 

```shell
pip install -r requirements.txt
```

2. 使用 Docker 部署 Neo4j

```shell
make deploy-neo4j
```

3. 导入知识图谱数据

```shell
make import-data
```
