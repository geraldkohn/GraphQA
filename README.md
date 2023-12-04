# GraphQA 

Knowledge Graph-based Question-Answering System.

## 部署

* 安装 Python 依赖包 

```shell
pip install -r requirements.txt
```

* 使用 Docker 部署 Neo4j

```shell
make deploy-neo4j
```

* 启动

    * 导入全量数据并启动

    ```shell
    make run-all
    ```

    * 导入测试数据并启动
    ```shell
    make run-test
    ```
