import ahocorasick

from graph import GraphMessage
from const import GraphLabel, IntentionCategory, QueryWordCollection

class IntentionRecognize:
    """
    意图是通过 实体+查询词 构成的
    """
    
    def __init__(self, graph_message: GraphMessage, query_word_collection: QueryWordCollection):
        self.graph_message = graph_message
        self.query_words = query_word_collection
        self.search_entity_trie_tree = self._build_search_entity_trie_tree(self.graph_message)
        self.search_query_words_trie_tree = self._build_search_query_words_trie_tree(self.query_words)
        
    def _build_search_entity_trie_tree(self, graphMessage: GraphMessage):
        """
        构造前缀树, 用于匹配实体关键词和实体类别
        """
        trie_tree = ahocorasick.Automaton()
        trie_node_list = []
        for disease in graphMessage.diseases:
            trie_node_list.append(tuple([GraphLabel.Disease, disease["name"]]))
        for symptom in graphMessage.symptoms:
            trie_node_list.append(tuple([GraphLabel.Symptom, symptom]))
        for drug in graphMessage.drugs:
            trie_node_list.append(tuple([GraphLabel.Drug, drug]))
        for department in graphMessage.departments:
            trie_node_list.append(tuple([GraphLabel.Department, department]))
        for food in graphMessage.foods:
            trie_node_list.append(tuple([GraphLabel.Food, food]))
        for check in graphMessage.checks:
            trie_node_list.append(tuple([GraphLabel.Check, check]))
        for trie_node in trie_node_list:
            trie_tree.add_word(trie_node[1], trie_node)
        trie_tree.make_automaton()
        return trie_tree
    
    def _build_search_query_words_trie_tree(self, queryWordCollection: QueryWordCollection):
        """
        构造前缀树, 用于匹配查询疑问词和疑问词类别
        """
        trie_tree = ahocorasick.Automaton()
        trie_node_list = []
        for query_word in queryWordCollection.query_word_list:
            for word in query_word.word_list:
                trie_node_list.append(tuple([query_word.uid, word]))
        for trie_node in trie_node_list:
            trie_tree.add_word(trie_node[1], trie_node)
        trie_tree.make_automaton()
        return trie_tree
    
    def _entity_list_to_dict(self, entity_list: list[tuple[GraphLabel, str]]) -> dict[GraphLabel, list[str]]:
        label_map: dict[GraphLabel, list[str]] = {}
        for element in entity_list:
            if element[0] in label_map:
                label_map[element[0]].append(element[1])
            else:
                label_map[element[0]] = [element[1]]
        
        return label_map
        
    def classify(self, normal_language_question: str) -> tuple[IntentionCategory, dict[GraphLabel, list[str]]]:
        """
        根据查询关键词和查询中实体来分析意图, 返回意图和实体 
        """
        
        # 实体列表
        entity_list: list[tuple[GraphLabel, str]] = []
        # 查询关键词列表
        query_word_list: list[tuple[int, str]] = []
        for result in self.search_entity_trie_tree.iter(normal_language_question):
            entity_list.append(result[1])
        for result in self.search_query_words_trie_tree.iter(normal_language_question):
            query_word_list.append(result[1])
        
        # 实体类别
        label_set = set(value[0] for value in entity_list)
        # 查询关键词类别
        uid_set = set(value[0] for value in query_word_list)
        
        # 疾病描述
        # 暂时没想好怎么匹配
        
        # 疾病预防措施
        if (GraphLabel.Disease in label_set) and (self.query_words.Prevent.uid in uid_set):
            return IntentionCategory.DiseasePrevent, self._entity_list_to_dict(entity_list)
        # 疾病病因
        elif (GraphLabel.Disease in label_set) and (self.query_words.Why.uid in uid_set):
            return IntentionCategory.DiseaseCause, self._entity_list_to_dict(entity_list)
        # 疾病染病概率
        elif (GraphLabel.Disease in label_set) and (self.query_words.GetSick.uid in uid_set) and (self.query_words.Prob.uid in uid_set):
            return IntentionCategory.DiseaseGetProb, self._entity_list_to_dict(entity_list)
        # 疾病染病方式
        elif (GraphLabel.Disease in label_set) and (self.query_words.GetSick.uid in uid_set) and (self.query_words.How.uid in uid_set):
            return IntentionCategory.DiseaseGetWay, self._entity_list_to_dict(entity_list)
        # 疾病易感染人群
        elif (GraphLabel.Disease in label_set) and (self.query_words.GetSick.uid in uid_set) and (self.query_words.People.uid in uid_set):
            return IntentionCategory.DiseasePeopleEasyGet, self._entity_list_to_dict(entity_list)
        # 疾病治疗方法
        elif (GraphLabel.Disease in label_set) and (self.query_words.Treat.uid in uid_set) and (self.query_words.How.uid in uid_set):
            return IntentionCategory.DiseaseCureWay, self._entity_list_to_dict(entity_list)
        # 疾病治愈时长
        elif (GraphLabel.Disease in label_set) and (self.query_words.Treat.uid in uid_set) and (self.query_words.Time.uid in uid_set):
            return IntentionCategory.DiseaseCureTime, self._entity_list_to_dict(entity_list)
        # 疾病治愈概率
        elif (GraphLabel.Disease in label_set) and (self.query_words.Treat.uid in uid_set) and (self.query_words.Prob.uid in uid_set):
            return IntentionCategory.DiseaseCureProb, self._entity_list_to_dict(entity_list)
        
        # 得了该疾病不能吃什么
        elif (GraphLabel.Disease in label_set) and (self.query_words.No.uid in uid_set) and (self.query_words.Eat.uid in uid_set):
            return IntentionCategory.DiseaseShouldNotEat, self._entity_list_to_dict(entity_list)
        # 得了该疾病应该吃什么
        elif (GraphLabel.Disease in label_set) and (self.query_words.Eat.uid in uid_set):
            return IntentionCategory.DiseaseShouldEat, self._entity_list_to_dict(entity_list)
        # 疾病推荐药品
        elif (GraphLabel.Disease in label_set) and (self.query_words.Drug.uid in uid_set):
            return IntentionCategory.DiseaseDrug, self._entity_list_to_dict(entity_list)
        # 得了疾病要做的检查
        elif (GraphLabel.Disease in label_set) and (self.query_words.Check.uid in uid_set):
            return IntentionCategory.DiseaseCheck, self._entity_list_to_dict(entity_list)
        # 疾病的症状
        elif (GraphLabel.Disease in label_set) and (self.query_words.Symptom.uid in uid_set):
            return IntentionCategory.DiseaseSymptom, self._entity_list_to_dict(entity_list)
        # 疾病的并发症
        elif (GraphLabel.Disease in label_set) and (self.query_words.Coexist.uid in uid_set):
            return IntentionCategory.DiseaseCoExist, self._entity_list_to_dict(entity_list)
        # 疾病属于的科室
        elif (GraphLabel.Disease in label_set) and (self.query_words.Department.uid in uid_set):
            return IntentionCategory.DiseaseDepartment, self._entity_list_to_dict(entity_list)
        
        # 查询症状会导致哪些疾病
        elif (GraphLabel.Symptom in label_set) and (self.query_words.Disease.uid in uid_set):
            return IntentionCategory.SymptomDisease, self._entity_list_to_dict(entity_list)
        # 查询药物可以治疗哪些疾病
        elif (GraphLabel.Drug in label_set) and (self.query_words.Treat.uid in uid_set):
            return IntentionCategory.DrugDisease, self._entity_list_to_dict(entity_list)
        # 查询科室可以诊断哪些疾病
        elif (GraphLabel.Department in label_set) and ((self.query_words.Treat.uid in uid_set) or (self.query_words.Diagnose.uid in uid_set)):
            return IntentionCategory.DepartmentDisease, self._entity_list_to_dict(entity_list)
        # 查询此检查还可以被哪些疾病需要
        elif (GraphLabel.Check in label_set) and ((self.query_words.Check.uid in uid_set) or (self.query_words.Disease.uid in uid_set)):
            return IntentionCategory.CheckDisease, self._entity_list_to_dict(entity_list)
        # Not Support
        else:
            return IntentionCategory.NotSupport, {}
