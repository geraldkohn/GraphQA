from const import IntentionCategory

def handle_DiseaseDesc(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.description"
    
def handle_DiseasePrevent(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.prevent"

def handle_DiseaseCause(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.cause"

def handle_DiseaseGetProb(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.get_prob"

def handle_DiseaseGetWay(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.get_way"

def handle_DiseasePeopleEasyGet(disease_name: str) -> str:
    return f"MATCH (m:Disease) where m.name = '{disease_name}' return m.name, m.people_easy_get"

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
    return f"MATCH (m:Disease)-[r:has_symptom]->(n:Symptom) where n.name = '{symptom_name}' return m.name, r.name, n.name"

def handle_DrugDisease(drug_name: str) -> str:
    return f"MATCH (m:Disease)-[r:recommand_drug]->(n:Drug) where n.name = '{drug_name}' return m.name, r.name, n.name"

def handle_DepartmentDisease(department_name: str) -> str:
    return f"MATCH (m:Disease)-[r:belong_to]->(n:Department) where n.name = '{department_name}' return m.name, r.name, n.name "

def handle_CheckDisease(check_name: str) -> str:
    return f"MATCH (m:Disease)-[r:need_check]->(n:Check) where n.name = '{check_name}' return m.name, r.name, n.name"

def handle_NotSupportQuery() -> str:
    return "not_support"

class IntentionQueryToSQL:
    def __init__(self):
        self.query_dict = {
            IntentionCategory.DiseaseDesc: handle_DiseaseDesc,
            IntentionCategory.DiseasePrevent: handle_DiseasePrevent,
            IntentionCategory.DiseaseCause: handle_DiseaseCause,
            IntentionCategory.DiseaseGetProb: handle_DiseaseGetProb,
            IntentionCategory.DiseaseGetWay: handle_DiseaseGetWay,
            IntentionCategory.DiseasePeopleEasyGet: handle_DiseasePeopleEasyGet,
            IntentionCategory.DiseaseCureWay: handle_DiseaseCureWay,
            IntentionCategory.DiseaseCureTime: handle_DiseaseCureTime,
            IntentionCategory.DiseaseCureProb: handle_DiseaseCureProb,
            
            IntentionCategory.DiseaseShouldEat: handle_DiseaseShouldEat,
            IntentionCategory.DiseaseShouldNotEat: handle_DiseaseShouldNotEat,
            IntentionCategory.DiseaseDrug: handle_DiseaseDrug,
            IntentionCategory.DiseaseCheck: handle_DiseaseCheck,
            IntentionCategory.DiseaseCoExist: handle_DiseaseCoExist,
            IntentionCategory.DiseaseDepartment: handle_DiseaseDepartment,
            
            IntentionCategory.SymptomDisease: handle_SymptomDisease,
            IntentionCategory.DrugDisease: handle_DrugDisease,
            IntentionCategory.DepartmentDisease: handle_DepartmentDisease,
            IntentionCategory.CheckDisease: handle_CheckDisease,
            
            IntentionCategory.NotSupport: handle_NotSupportQuery,
        }

    def intention_query_to_sql(self, query_intention: IntentionCategory) -> str:
        '''
        根据意图使用知识图谱查询语言, 完成查询
        '''
        sql = self.query_dict.get(query_intention, IntentionCategory.NotSupport)()
        return sql
