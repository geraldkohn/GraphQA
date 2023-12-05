import json
from py2neo import Graph, Node

from utils import logger
from const import GraphLabel
from config import Config

class GraphMessage:
    def __init__(self):
        # 节点
        self.diseases = []       # 疾病
        self.symptoms = []       # 症状
        self.drugs = []          # 药品
        self.departments = []    # 科室
        self.foods = []          # 食物
        self.checks = []         # 检查

        # 关系
        self.disease_not_eat = []           # 疾病--忌吃食物关系
        self.disease_do_eat = []            # 疾病--宜吃食物关系
        self.disease_drug = []              # 疾病--药品关系
        self.disease_check = []             # 疾病--检查关系
        self.disease_symptom = []           # 疾病--症状关系
        self.disease_disease_coexist = []   # 疾病--疾病关系 (并发疾病)
        self.disease_department = []        # 疾病--科室关系

class DataLoader:
    def __init__(self, data_path: str):
        self.data_path = data_path
        self.graph = GraphMessage()
        
        self._attr_name = 'name'
        self._attr_department = 'department'
        self._attr_symptom = 'symptom'
        self._attr_drug = 'drug'
        self._attr_should_eat = 'should_eat'
        self._attr_should_not_eat = 'should_not_eat'
        self._attr_check = 'check'
        self._attr_coexist_disease = 'coexist_disease'
        
        self._attr_description = 'description'
        self._attr_prevent = 'prevent'
        self._attr_cause = 'cause'
        self._attr_get_prob = 'get_prob'
        self._attr_get_way = 'get_way'
        self._attr_people_easy_get = 'people_easy_get'
        self._attr_cure_way = 'cure_way'
        self._attr_cure_time = 'cure_time'
        self._attr_cure_prob = 'cure_prob'
        
        self._disease_info = [self._attr_name, self._attr_description, self._attr_prevent, self._attr_cause, self._attr_get_prob, self._attr_get_way, self._attr_people_easy_get, self._attr_cure_way, self._attr_cure_time, self._attr_cure_prob]
    
    def load(self):
        logger.info(f"正在加载数据...")
        cnt = 1
        with open(self.data_path, "r") as file:
            line = file.readline()
            while line:
                line_dict = json.loads(line.strip())
                self._handle_single_line(graph=self.graph, data=line_dict)
                line = file.readline()
                cnt = cnt+1
            logger.info(f"加载数据成功! 共{cnt}行数据")
    
    def get_graph(self) -> GraphMessage:
        return self.graph
                
    def _handle_single_line(self, graph: GraphMessage, data: dict):
        disease = {}
        for info in self._disease_info:
            if info in data:
                disease[info] = data[info]
        graph.diseases.append(disease)
        
        disease_name = data[self._attr_name]
        
        if self._attr_department in data:
            departments = data[self._attr_department]
            for value in departments:
                if value not in graph.departments:
                    graph.departments.append(value)
                relation = [disease_name, value]
                if relation not in graph.disease_department:
                    graph.disease_department.append(relation)
                    
        if self._attr_symptom in data:
            symptoms = data[self._attr_symptom]
            for value in symptoms:
                if value not in graph.symptoms:
                    graph.symptoms.append(value)
                relation = [disease_name, value]
                if relation not in graph.disease_symptom:
                    graph.disease_symptom.append(relation)
                    
        if self._attr_drug in data:
            drugs = data[self._attr_drug]
            for value in drugs:
                if value not in graph.drugs:
                    graph.drugs.append(value)
                relation = [disease_name, value]
                if relation not in graph.disease_symptom:
                    graph.disease_drug.append(relation)
                    
        if self._attr_should_eat in data:
            should_eat_foods = data[self._attr_should_eat]
            for value in should_eat_foods:
                if value not in graph.foods:
                    graph.foods.append(value)
                relation = [disease_name, value]
                if relation not in graph.disease_symptom:
                    graph.disease_do_eat.append(relation)
                
        if self._attr_should_not_eat in data:
            should_not_eat_foods = data[self._attr_should_not_eat]
            for value in should_not_eat_foods:
                if value not in graph.foods:
                    graph.foods.append(value)
                relation = [disease_name, value]
                if relation not in graph.disease_symptom:
                    graph.disease_not_eat.append(relation)
                
        if self._attr_check in data:
            checks = data[self._attr_check]
            for value in checks:
                if value not in graph.checks:
                    graph.checks.append(value)
                relation = [disease_name, value]
                if relation not in graph.disease_symptom:
                    graph.disease_check.append(relation)
                
        if self._attr_coexist_disease in data:
            coexist_disease = data[self._attr_coexist_disease]
            for value in coexist_disease:
                relation = [disease_name, value]
                if relation not in graph.disease_disease_coexist:
                    graph.disease_disease_coexist.append(relation)

class GraphBuilder:
    def __init__(self, graph: GraphMessage):
        self._config = Config()
        self._neo4j_driver = Graph('bolt://{}:{}'.format(self._config.neo4j_host, self._config.neo4j_port), auth=(self._config.neo4j_user, self._config.neo4j_password))
        self.graph = graph
    
    def _build_disease_node(self, disease: dict):
        node = Node(GraphLabel.Disease.value, **disease)
        try:
            self._neo4j_driver.create(node)
        except Exception as e:
            logger.error(f"导入节点失败: {e} | 节点类型: Disease")
    
    def _build_normal_node(self, label: str, node_name: str):
        node = Node(label, name=node_name)
        try: 
            self._neo4j_driver.create(node)
        except Exception as e:
            logger.error(f"导入节点失败: {e} | 节点类型: {label}")
    
    def _build_edge(self, start_node_label: str, end_node_label: str, start_node_name: str, end_node_name: str, relation_type: str, relation_name: str):
        query = "match(p:%s),(q:%s) where p.name='%s' and q.name='%s' create (p)-[relation:%s{name:'%s'}]->(q)" % (start_node_label, end_node_label, start_node_name, end_node_name, relation_type, relation_name)
        try:
            summery = self._neo4j_driver.run(query).summary
        except Exception as e:
            logger.error(f"导入边失败: {e} | 开始节点: {start_node_label} {start_node_name} | 终止节点: {end_node_label} {end_node_name} | 边的类型: {relation_type} {relation_name}")
    
    def build_nodes(self):
        try:
            logger.info(f"正在导入节点数据到 Neo4j ...")
        
            logger.info(f"正在导入 疾病 节点 ..., 共 {len(self.graph.diseases)} 条")
            for disease_dict in self.graph.diseases:
                self._build_disease_node(disease=disease_dict)
            
            logger.info(f"正在导入 症状 节点 ..., 共 {len(self.graph.symptoms)} 条")
            for symptom_name in self.graph.symptoms:
                self._build_normal_node(label=GraphLabel.Symptom.value, node_name=symptom_name)
            
            logger.info(f"正在导入 药品 节点 ..., 共 {len(self.graph.drugs)} 条")
            for drug_name in self.graph.drugs:
                self._build_normal_node(label=GraphLabel.Drug.value, node_name=drug_name)
            
            logger.info(f"正在导入 科室 节点 ..., 共 {len(self.graph.departments)} 条")
            for department_name in self.graph.departments:
                self._build_normal_node(label=GraphLabel.Department.value, node_name=department_name)
        
            logger.info(f"正在导入 食物 节点 ..., 共 {len(self.graph.foods)} 条")
            for food_name in self.graph.foods:
                self._build_normal_node(label=GraphLabel.Food.value, node_name=food_name)
            
            logger.info(f"正在导入 检查 节点 ..., 共 {len(self.graph.checks)} 条")
            for check_name in self.graph.checks:
                self._build_normal_node(label=GraphLabel.Check.value, node_name=check_name)
        except Exception as e:
            logger.error(f"导入节点数据到 Neo4j 时抛出异常: {e}")
        
    def build_edges(self):
        try: 
            logger.info(f"正在导入边数据到 Neo4j ...")
        
            logger.info(f"正在导入 忌吃 边 ..., 共 {len(self.graph.disease_not_eat)} 条")
            for edge in self.graph.disease_not_eat:
                if len(edge) >= 2:
                    self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Food.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.ShouldNotEat.value, relation_name='忌吃')
                else:
                    logger.error(f"边的长度小于2 | 边: {edge}")
            
            logger.info(f"正在导入 宜吃 边 ..., 共 {len(self.graph.disease_do_eat)} 条")
            for edge in self.graph.disease_do_eat:
                if len(edge) >= 2:
                    self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Food.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.ShouldEat.value, relation_name='宜吃')
                else:
                    logger.error(f"边的长度小于2 | 边: {edge}")
            
            logger.info(f"正在导入 推荐用药 边 ..., 共 {len(self.graph.disease_drug)} 条")
            for edge in self.graph.disease_drug:
                if len(edge) >= 2:
                    self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Drug.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.RecommandDrug.value, relation_name='推荐用药')
                else:
                    logger.error(f"边的长度小于2 | 边: {edge}")
            
            logger.info(f"正在导入 需要做的检查 边 ..., 共 {len(self.graph.disease_check)} 条")
            for edge in self.graph.disease_check:
                self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Check.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.NeedCheck.value, relation_name='需要做的检查')
            
            logger.info(f"正在导入 症状 边 ..., 共 {len(self.graph.disease_symptom)} 条")
            for edge in self.graph.symptoms:
                if len(edge) >= 2:
                    self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Symptom.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.HasSymptom.value, relation_name='症状')
                else:
                    logger.error(f"边的长度小于2 | 边: {edge}")
            
            logger.info(f"正在导入 并发症 边 ..., 共 {len(self.graph.disease_disease_coexist)} 条")
            for edge in self.graph.disease_disease_coexist:
                if len(edge) >= 2:
                    self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Disease.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.AcompanyWith.value, relation_name='并发症')
                else:
                    logger.error(f"边的长度小于2 | 边: {edge}")
            
            logger.info(f"正在导入 所属科室 边 ..., 共 {len(self.graph.disease_department)} 条")
            for edge in self.graph.disease_department:
                if len(edge) >= 2:
                    self._build_edge(start_node_label=GraphLabel.Disease.value, end_node_label=GraphLabel.Department.value, start_node_name=edge[0], end_node_name=edge[1], relation_type=GraphLabel.BelongTo.value, relation_name='所属科室')
                else:
                    logger.error(f"边的长度小于2 | 边: {edge}")
        except Exception as e:
            logger.error(f"导入边数据到 Neo4j 时抛出异常: {e}")
