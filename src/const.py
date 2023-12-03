from enum import Enum

class GraphLabel(Enum):
    # Node Label
    Disease = "Disease"
    Symptom = "Symptom"
    Drug = "Drug"
    Department = "Department"
    Food = "Food"
    Check = "Check"
    
    # Relation Label
    ShouldNotEat = "should_not_eat"
    ShouldEat = "should_eat"
    RecommandDrug = "recommand_drug"
    NeedCheck = "need_check"
    HasSymptom = "has_symptom"
    AcompanyWith = "acompany_with"
    BelongTo = "belong_to"

class IntentionCategory(Enum):
    # Disease Info
    DiseaseDesc = "DiseaseDesc" # 疾病描述
    DiseasePrevent = "DiseasePrevent" # 疾病预防措施
    DiseaseCause = "DiseaseCause" # 疾病原因
    DiseaseGetProb = "DiseaseGetProb" # 疾病染病概率
    DiseaseGetWay = "DiseaseGetWay" # 疾病染病方式
    DiseasePeopleEasyGet = "DiseasePeopleEasyGet" # 疾病易感染人群
    DiseaseCureWay = "DiseaseCureWay" # 疾病治疗方法
    DiseaseCureTime = "DiseaseCureTime" # 疾病治愈时长
    DiseaseCureProb = "DiseaseCureProb" # 疾病治愈概率
    
    # Relations From Disease To Others
    DiseaseShouldNotEat = "DiseaseShouldNotEat" # 得了该疾病不能吃什么
    DiseaseShouldEat = "DiseaseShouldEat" # 得了该疾病应该吃什么
    DiseaseDrug = "DiseaseDrug" # 疾病推荐药品
    DiseaseCheck = "DiseaseCheck" # 得了疾病要做的检查
    DiseaseSymptom = "DiseaseSymptom" # 疾病的症状
    DiseaseCoExist = "DiseaseCoExist" # 疾病的并发症
    DiseaseDepartment = "DiseaseDepartment" # 疾病属于的科室
    
    # Relations From Others To Disease
    SymptomDisease = "SymptomDisease" # 查询症可能患有哪些疾病
    DrugDisease = "DrugDisease" # 查询药物可以治疗哪些疾病
    DepartmentDisease = "DepartmentDisease" # 查询科室可以诊断哪些疾病
    CheckDisease = "CheckDisease" # 查询此检查还可以被哪些疾病需要
    
    # Not Support
    NotSupport = "NotSupport"

class QueryWordCollection:
    def __init__(self):
        self.Why = QueryWord(1, ['为什么', '原因', '起因', '病因', '因素', '引起'])
        self.What = QueryWord(2, ['什么'])
        self.How = QueryWord(3, ['怎么', '如何', '方式', '怎样'])
        self.Symptom = QueryWord(4, ['症状', '表征', '现象', '症候', '表现'])
        self.Coexist = QueryWord(5, ['并发', '一起', '一并', '一同', '伴随', '共现'])
        self.Eat = QueryWord(6, ['饮食', '喝', '菜', '忌口', '东西'])
        self.Drug = QueryWord(7, ['药'])
        self.Prevent = QueryWord(8, ['预防', '防止', '避免'])
        self.No = QueryWord(9, ['不', '忌'])
        self.Time = QueryWord(10, ['周期', '时间', '天', '月', '年', '久'])
        self.Treat = QueryWord(11, ['医疗', '康复', '恢复', '治', '有效', '见效', '起效果'])
        self.GetSick = QueryWord(12, ['感染', '染上', '患病', '得', '传染'])
        self.Prob = QueryWord(13, ['概率', '几率', '希望', '几成', '比例', '可能性', '把握'])
        self.People = QueryWord(14, ['人'])
        self.Check = QueryWord(165, ['检查', '仪器'])
        self.Department = QueryWord(16, ['部门', '科'])
        self.Disease = QueryWord(17, ['病', '症'])
        self.Diagnose = QueryWord(18, ['诊断'])
        
        self.query_word_list = [self.Symptom, self.Why, self.What, self.Coexist, self.Eat, self.Drug, self.Prevent, self.No, self.Time, self.How, self.Treat, self.GetSick, self.Prob, self.People, self.Check, self.Department, self.Disease, self.Diagnose]

class QueryWord:
    def __init__(self, category: int, word_list: list[str]):
        self.uid = category
        self.word_list= word_list

class DataSetAttribute(Enum):
    pass
