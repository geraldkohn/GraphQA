import argparse
from utils import logger
from config import Config
from build_graph import DataLoader, GraphBuilder
from intention_recognize import IntentionRecognizer
from const import QueryWordCollection
from intention_to_cypher import CypherGenerater
from search_answer import GraphSearcher, AnswerGenerater

class GraphQA:
    def __init__(self, data_path: str):
        self.data_loader = DataLoader(data_path=data_path)
        self.data_loader.load()
        
        self.graph_builder = GraphBuilder(self.data_loader.graph)
        self.graph_builder.build_nodes()
        self.graph_builder.build_edges()
        
        self.intention_recognizer = IntentionRecognizer(self.data_loader.graph, QueryWordCollection())
        self.cypher_generater = CypherGenerater()
        self.graph_searcher = GraphSearcher()
        self.answer_generater = AnswerGenerater()
    
    def run(self, input: str) -> str:
        # 输入
        answers: list[str] = []
        
        intention, entity_map = self.intention_recognizer.classify(normal_language_question=input)
        logger.info(f"已分析到自然语言中存在的意图和实体 | 意图: {intention} | 实体: {entity_map}")
        
        cyphers = self.cypher_generater.generate(intention, entity_map)
        if len(cyphers) == 0:
            return self.answer_generater.no_data_answer
        for cypher in cyphers:
            search_result = self.graph_searcher.search(intention, cypher)
            answer = self.answer_generater.answer(intention, search_result)
            answers.append(answer)
            
        logger.info(f"得到的回答: {answers}")
        
        return '\n' + '\n'.join(answers)
    
    def console_loop(self):
        print("基于知识图谱的问答系统已启动, 请提问: (输入 'exit' 退出)")
        while True:
            user_input = input("> ")
            if user_input.lower() == 'exit':
                break
            else:
                answer = self.run(user_input)
                print(answer)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default="test")
    args = parser.parse_args()
    
    cfg = Config()
    
    data_path = ''
    
    if args.data == 'all':
        data_path = cfg.data_path
    else:
        data_path = cfg.test_data_path
    
    graphQA = GraphQA(data_path=data_path)
    graphQA.console_loop()
