from intention_recognize import IntentionRecognize
from graph import DataLoader
from const import QueryWordCollection
import config

def test_intention_recognize_classify():
    print("-----------------------------------测试意图识别-----------------------------------")
    
    cfg = config.Config()
    dataloader = DataLoader(cfg.test_data_path)
    dataloader.load()
    query_word_collection = QueryWordCollection()
    
    intention_recognize = IntentionRecognize(dataloader.graph, query_word_collection)
    
    query_list = [
        "如何预防脑血管病",
        "脑血管病是什么原因引起的",
        "正常人得脑血管病的概率是多少",
        "哪些人容易得脑血管病",
        "正常人是怎么得脑血管病的",
        "脑血管病怎么治疗",
        "脑血管病多长时间能康复",
        "脑血管病多大几率能够治愈",
        
        "得了脑血管病有哪些忌口",
        "得了脑血管病推荐吃什么东西",
        "得了脑血管病应该吃什么药",
        "得了脑血管病需要做哪些检查",
        "脑血管病的症状是什么",
        "脑血管病有哪些并发症",
        "脑血管病应该去哪个科室就诊",
        
        "血管堵塞可能是什么病",
        "尼莫地平片能治疗什么病",
        "内科都能诊断什么病",
        "什么病需要做脑血管造影",
    ]
    
    for query in query_list:
        intention, label_dict = intention_recognize.classify(query)
        print(f"query: {query} | intention: {intention} | label_dict: {label_dict}")
    
if __name__ == "__main__":
    # print_Buddha()
    test_intention_recognize_classify()
