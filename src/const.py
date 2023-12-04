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
    DiseaseDescription = 1 # 疾病描述
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
    SymptomDisease = 17 # 查询症可能患有哪些疾病
    DrugDisease = 18 # 查询药物可以治疗哪些疾病
    DepartmentDisease = 19 # 查询科室可以诊断哪些疾病
    CheckDisease = 20 # 查询此检查还可以被哪些疾病需要
    
    # Not Support
    NotSupport = 21

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
