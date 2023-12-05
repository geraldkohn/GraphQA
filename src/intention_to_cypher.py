from const import GraphLabel, IntentionCategory
from utils import logger

def handle_DiseaseDescription(disease_name: str) -> str:
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

class CypherGenerater:
    def __init__(self):
        pass
    
    def generate(self, intention: IntentionCategory, entity_map: dict[GraphLabel, list[str]]) -> list[str]:
        """
        根据意图和实体, 生成 Cypher 查询语句 
        """
        
        logger.info(f"根据意图和实体, 正在生成 Cypher 查询... | 意图: {intention} | 实体: {entity_map}")
        
        cyphers: list[str] = []
        
        if intention == IntentionCategory.DiseaseDescription:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseDescription(disease_name=disease))
        elif intention == IntentionCategory.DiseasePrevent:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseasePrevent(disease_name=disease))
        elif intention == IntentionCategory.DiseaseCause:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseCause(disease_name=disease))
        elif intention == IntentionCategory.DiseaseGetProb:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseGetProb(disease_name=disease))
        elif intention == IntentionCategory.DiseaseGetWay:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseGetWay(disease_name=disease))
        elif intention == IntentionCategory.DiseasePeopleEasyGet:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseasePeopleEasyGet(disease_name=disease))
        elif intention == IntentionCategory.DiseaseCureWay:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseCureWay(disease_name=disease))
        elif intention == IntentionCategory.DiseaseCureTime:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseCureTime(disease_name=disease))
        elif intention == IntentionCategory.DiseaseCureProb:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseCureProb(disease_name=disease))
        
        elif intention == IntentionCategory.DiseaseShouldNotEat:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseShouldNotEat(disease_name=disease))
        elif intention == IntentionCategory.DiseaseShouldEat:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseShouldEat(disease_name=disease))
        elif intention == IntentionCategory.DiseaseDrug:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseDrug(disease_name=disease))
        elif intention == IntentionCategory.DiseaseCheck:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseCheck(disease_name=disease))
        elif intention == IntentionCategory.DiseaseSymptom:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseSymptom(disease_name=disease))
        elif intention == IntentionCategory.DiseaseCoExist:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseCoExist(disease_name=disease))
        elif intention == IntentionCategory.DiseaseDepartment:
            for disease in entity_map[GraphLabel.Disease]:
                cyphers.append(handle_DiseaseDepartment(disease_name=disease))
       
        elif intention == IntentionCategory.SymptomDisease:
            for symptom in entity_map[GraphLabel.Symptom]:
                cyphers.append(handle_SymptomDisease(symptom_name=symptom))
        elif intention == IntentionCategory.DrugDisease:
            for drug in entity_map[GraphLabel.Drug]:
                cyphers.append(handle_DrugDisease(drug_name=drug))
        elif intention == IntentionCategory.DepartmentDisease:
            for department in entity_map[GraphLabel.Department]:
                cyphers.append(handle_DepartmentDisease(department_name=department))
        elif intention == IntentionCategory.CheckDisease:
            for check in entity_map[GraphLabel.Check]:
                cyphers.append(handle_CheckDisease(check_name=check))
        
        elif intention == IntentionCategory.NotSupport:
            pass
        
        else:
            pass
        
        logger.info(f"已生成 Cypher 查询 | 长度: {len(cyphers)} | 内容: {cyphers}")
        
        return cyphers
