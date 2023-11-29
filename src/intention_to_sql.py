from enum import Enum
from build_knowledge_graph import Neo4jLabel

class Intention(Enum):
    # Disease Info
    DiseaseDesc = 1 # 疾病症状
    DiseasePrevent = 2 # 疾病预防措施
    DiseaseCause = 3 # 疾病原因
    DiseaseGetProb = 4 # 疾病染病概率
    DiseaseGetWay = 5 # 疾病染病方式
    DiseasePeopleEasyGet = 6 # 疾病易感染人群
    DiseaseCureWay = 7 # 疾病治疗方法
    DiseaseCureTime = 8 # 疾病治愈时长
    DiseaseCureProb = 9 # 疾病治愈概率
    
    # Relations From Disease To Others
    DiseaseShouldNotEat = 10 # 得了该疾病不能吃什么
    DiseaseShouldEat = 11 # 得了该疾病应该吃什么
    DiseaseDrug = 12 # 疾病推荐药品
    DiseaseCheck = 13 # 得了疾病要做的检查
    DiseaseSymptom = 14 # 疾病的症状
    DiseaseCoExist = 15 # 疾病的并发症
    DiseaseDepartment = 16 # 疾病属于的科室
    
    # Relations From Others To Disease
    SymptomDisease = 17 # 查询症状会导致哪些疾病
    
    # Not Support
    NotSupportQuery = 18

def handle_DiseaseDesc(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.desc"
    
def handle_DiseasePrevent(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.prevent"

def handle_DiseaseCause(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.cause"

def handle_DiseaseGetProb(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.get_prob"

def handle_DiseaseGetWay(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.get_way"

def handle_DiseasePeopleEasyGet(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.easy_get"

def handle_DiseaseCureWay(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.cure_way"

def handle_DiseaseCureTime(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.cure_time"

def handle_DiseaseCureProb(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.cure_prob"

def handle_DiseaseShouldNotEat(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:should_not_eat]->(n:Food) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_DiseaseShouldEat(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:should_eat]->(n:Food) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_DiseaseDrug(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_DiseaseCheck(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:need_check]->(n:Check) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_DiseaseSymptom(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_DiseaseCoExist(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:acompany_with]->(n:Disease) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_DiseaseDepartment(disease_name: str) -> str:
    return f"MATCH (m:Disease)-[r:belong_to]->(n:Department) where m.name = '{disease_name}' return m.name, r.name, n.name"

def handle_SymptomDisease(symptom_name: str) -> str:
    return f"MATCH (m:Disease)-[r:has_symptom]->(n:Department) where n.name = '{symptom_name}' return m.name, r.name, n.name"

def handle_NotSupportQuery() -> str:
    return "not_support"

class IntentionQueryToSQL:
    def __init__(self):
        self.query_dict = {
            Intention.DiseaseDesc: handle_DiseaseDesc,
            Intention.DiseasePrevent: handle_DiseasePrevent,
            Intention.DiseaseCause: handle_DiseaseCause,
            Intention.DiseaseGetProb: handle_DiseaseGetProb,
            Intention.DiseaseGetWay: handle_DiseaseGetWay,
            Intention.DiseasePeopleEasyGet: handle_DiseasePeopleEasyGet,
            Intention.DiseaseCureWay: handle_DiseaseCureWay,
            Intention.DiseaseCureTime: handle_DiseaseCureTime,
            Intention.DiseaseCureProb: handle_DiseaseCureProb,
            
            Intention.DiseaseShouldEat: handle_DiseaseShouldEat,
            Intention.DiseaseShouldNotEat: handle_DiseaseShouldNotEat,
            Intention.DiseaseDrug: handle_DiseaseDrug,
            Intention.DiseaseCheck: handle_DiseaseCheck,
            Intention.DiseaseCoExist: handle_DiseaseCoExist,
            Intention.DiseaseDepartment: handle_DiseaseDepartment,
            
            Intention.SymptomDisease: handle_SymptomDisease,
            
            Intention.NotSupportQuery: handle_NotSupportQuery,
        }

    def intention_query_to_sql(self, query_intention: Intention) -> str:
        '''
        根据意图使用知识图谱查询语言, 完成查询
        '''
        sql = self.query_dict.get(query_intention, Intention.NotSupportQuery)()
        return sql
