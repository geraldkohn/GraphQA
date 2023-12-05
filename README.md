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

    * 导入全量数据到 Neo4j 并启动全量数据问答系统

    ```shell
    make run-all
    ```

    * 导入测试数据到 Neo4j 并启动测试数据问答系统
    ```shell
    make run-test
    ```

    * 重启全量数据问答系统
    ```shell
    make restart-all
    ```

    * 重启测试数据问答系统
    ```shell
    make restart-test
    ```

## 测试

* 如何预防青春期厌食症

* 青春期厌食症的病因是什么

* 健康的人患有青春期厌食症的几率有多大

* 哪些人容易得青春期厌食症

* 青春期厌食症是如何传染的

* 青春期厌食症怎么治疗

* 青春期厌食症多长时间能康复

* 青春期厌食症有多大几率被治愈

* 得了青春期厌食症有哪些忌口

* 得了青春期厌食症推荐吃哪些东西

* 得了青春期厌食症应该吃什么药

* 得了青春期厌食症应该做哪些检查

* 青春期厌食症的症状是什么 ??

* 青春期厌食症有哪些并发症

* 青春期厌食症应该去哪个科室就诊

* 情绪性厌食可能是什么病 ??

* 五维牛磺酸口服溶液能治疗什么病

* 消化内科能诊断什么病

* 什么病需要做尿常规
