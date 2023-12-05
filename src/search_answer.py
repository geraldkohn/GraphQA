from py2neo import Graph

from config import Config
from const import IntentionCategory
from utils import logger


class GraphSearcher:
    def __init__(self):
        self._config = Config()
        self._neo4j_driver = Graph('bolt://{}:{}'.format(self._config.neo4j_host, self._config.neo4j_port), auth=(self._config.neo4j_user, self._config.neo4j_password))
    
    def search(self, intention: IntentionCategory, sql: str) -> list[dict]:
        logger.info(f"正在根据 Cypher 语句查询 Neo4j 数据库... | 意图: {intention} | 查询语句: {sql}")
        if intention == IntentionCategory.NotSupport:
            return []
        res = []
        try:
            res = self._neo4j_driver.run(sql).data()
        except Exception as e:
            logger.error(f"查询 Neo4j 失败: {e}")
        finally:
            return self._handle_result_from_neo4j(intention=intention, result_list=res)
    
    def _handle_result_from_neo4j(self, intention: IntentionCategory, result_list: list[dict]) -> list[dict]:
        """
        处理 Neo4j 返回字典的 key-value 
        """
        
        logger.info(f"正在转换 Neo4j 数据库的返回结果... | 意图: {intention} | Neo4j 原始返回结果: {result_list}")
        
        if len(result_list) == 0:
            return result_list
        
        handled_list: list[dict[str, str]] = []
        
        if intention == IntentionCategory.DiseaseDescription:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "description": result["m.description"]})
        elif intention == IntentionCategory.DiseasePrevent:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "prevent": result["m.prevent"]})
        elif intention == IntentionCategory.DiseaseCause:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "cause": result["m.cause"]})
        elif intention == IntentionCategory.DiseaseGetProb:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "get_prob": result["m.get_prob"]})
        elif intention == IntentionCategory.DiseaseGetWay:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "get_way": result["m.get_way"]})
            return handled_list
        elif intention == IntentionCategory.DiseasePeopleEasyGet:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "people_easy_get": result["m.people_easy_get"]})
        elif intention == IntentionCategory.DiseaseCureWay:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "cure_way": result["m.cure_way"]})
        elif intention == IntentionCategory.DiseaseCureTime:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "cure_time": result["m.cure_time"]})
        elif intention == IntentionCategory.DiseaseCureProb:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "cure_prob": result["m.cure_prob"]})
                
        elif intention == IntentionCategory.DiseaseShouldNotEat:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "food": result["n.name"]})
        elif intention == IntentionCategory.DiseaseShouldEat:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "food": result["n.name"]})
        elif intention == IntentionCategory.DiseaseDrug:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "drug": result["n.name"]})
        elif intention == IntentionCategory.DiseaseCheck:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "check": result["n.name"]})
        elif intention == IntentionCategory.DiseaseSymptom:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "symptom": result["n.name"]})
        elif intention == IntentionCategory.DiseaseCoExist:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "coexist": result["n.name"]})
        elif intention == IntentionCategory.DiseaseDepartment:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "department": result["n.name"]})
        
        elif intention == IntentionCategory.SymptomDisease:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "symptom": result["n.name"]})
        elif intention == IntentionCategory.DrugDisease:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "drug": result["n.name"]})
        elif intention == IntentionCategory.DepartmentDisease:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "department": result["n.name"]})
        elif intention == IntentionCategory.CheckDisease:
            for result in result_list:
                handled_list.append({"disease": result["m.name"], "r": result["r.name"], "check": result["n.name"]})
        
        elif intention == IntentionCategory.NotSupport:
            pass
        
        logger.info(f"转换完毕, 转换后 Neo4j 查询结果如下 | 意图: {intention} | 转换后结果: {handled_list}")
        
        return handled_list

        
class AnswerGenerater:
    def __init__(self):
        self.not_support_answer = "抱歉, 我没能理解您的意思, 请换一种问法"
        self.no_data_answer = "抱歉, 您问的相关信息还未收录到数据库中, 我无法回答"
    
    def answer(self, intention: IntentionCategory, search_result: list[dict]) -> str:
        logger.info(f"正在根据意图和实体做出回答... | 意图: {intention} | 实体: {search_result}")
        
        if len(search_result) == 0:
            return self.no_data_answer
        
        """ 
        Neo4j 查找返回的数据就类似于一个表结构
        
            x           y           z
        1  xxx         yyy      [zzz, zzz]
        2  xxx         yyy      [zzz, zzz]
        3  xxx         yyy      [zzz, zzz]
        4  xxx         yyy      [zzz, zzz]
        """
        
        obj: list[str] = []
        answer = ""
        
        # 这里的 result 就相当于表的一行
        if intention == IntentionCategory.DiseaseDescription:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["decription"], list):
                    for value in result["decription"]:
                        obj.append(value)
                else:
                    obj.append(result["decription"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的医学详细描述为: {', '.join(obj)}"
        
        elif intention == IntentionCategory.DiseasePrevent:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["prevent"], list):
                    for value in result["prevent"]:
                        obj.append(value)
                else:
                    obj.append(result["prevent"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的预防措施是: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseCause:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["cause"], list):
                    for value in result["cause"]:
                        obj.append(value)
                else:
                    obj.append(result["cause"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的患病原因是: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseGetProb:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["get_prob"], list):
                    for value in result["get_prob"]:
                        obj.append(value)
                else:
                    obj.append(result["get_prob"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的患病几率是: {', '.join(obj)}"    
            
        elif intention == IntentionCategory.DiseaseGetWay:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["get_way"], list):
                    for value in result["get_way"]:
                        obj.append(value)
                else:
                    obj.append(result["get_way"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的传播途径为: {', '.join(obj)}"
                
        elif intention == IntentionCategory.DiseasePeopleEasyGet:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["people_easy_get"], list):
                    for value in result["people_easy_get"]:
                        obj.append(value)
                else:
                    obj.append(result["people_easy_get"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的易患病群体为: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseCureWay:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["cure_way"], list):
                    for value in result["cure_way"]:
                        obj.append(value)
                else:
                    obj.append(result["cure_way"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的治疗方式有: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseCureTime:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["cure_time"], list):
                    for value in result["cure_time"]:
                        obj.append(value)
                else:
                    obj.append(result["cure_time"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的康复时间大概是: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseCureProb:
            disease = search_result[0]["disease"]
            for result in search_result:
                if isinstance(result["cure_prob"], list):
                    for value in result["cure_prob"]:
                        obj.append(value)
                else:
                    obj.append(result["cure_prob"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的治愈几率大概是: {', '.join(obj)}"
                
        # -------------------------------------------------------------
                
        elif intention == IntentionCategory.DiseaseShouldNotEat:
            disease = search_result[0]["disease"]
            for result in search_result:                    
                obj.append(result["food"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"患有{disease}需要忌口的食物有: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseShouldEat:
            disease = search_result[0]["disease"]
            for result in search_result:
                obj.append(result["food"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"患有{disease}推荐吃的食物有: {', '.join(obj)}"
                
        elif intention == IntentionCategory.DiseaseDrug:
            disease = search_result[0]["disease"]
            for result in search_result:
                obj.append(result["drug"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"针对{disease}, 推荐服用: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseCheck:
            disease = search_result[0]["disease"]
            for result in search_result:
                obj.append(result["check"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}需要做{', '.join(obj)}等检查项目"
            
        elif intention == IntentionCategory.DiseaseSymptom:
            disease = search_result[0]["disease"]
            for result in search_result:
                obj.append(result["symptom"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}的症状通常表现为: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseCoExist:
            disease = search_result[0]["disease"]
            for result in search_result:
                obj.append(result["coexist"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}常见的并发症有: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DiseaseDepartment:
            disease = search_result[0]["disease"]
            for result in search_result:
                obj.append(result["department"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{disease}应该去{', '.join(obj)}做检查"
                
        # -------------------------------------------------------------
        
        elif intention == IntentionCategory.SymptomDisease:
            symptom = search_result[0]["symptom"]
            for result in search_result:
                obj.append(result["disease"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"与症状{symptom}相关联的疾病为: {', '.join(obj)}"
            
        elif intention == IntentionCategory.DrugDisease:
            drug = search_result[0]["drug"]
            for result in search_result:
                obj.append(result["disease"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{drug}对{', '.join(obj)}起效果"
            
        elif intention == IntentionCategory.DepartmentDisease:
            department = search_result[0]["department"]
            for result in search_result:
                obj.append(result["disease"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"{department}可以诊治的疾病有: {', '.join(obj)}"
            
        elif intention == IntentionCategory.CheckDisease:
            check = search_result[0]["check"]
            for result in search_result:
                obj.append(result["disease"])
            if len(obj) == 0:
                answer = self.no_data_answer
            else:
                answer = f"患有{', '.join(obj)}需要做这个检查项目"
        
        elif intention == IntentionCategory.NotSupport:
            answer = self.not_support_answer
            
        else:
            answer = self.not_support_answer

        logger.info(f"问答系统做出的回答: {answer}")
        return answer
        