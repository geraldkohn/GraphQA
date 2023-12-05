import argparse
from utils import logger
from config import Config
from build_graph import DataLoader, GraphBuilder, GraphMessage
from intention_recognize import IntentionRecognizer
from const import QueryWordCollection
from intention_to_cypher import CypherGenerater
from search_answer import GraphSearcher, AnswerGenerater

class GraphQA:
    def __init__(self, data_path: str):
        self.data_path = data_path
            
    def import_data_to_neo4j(self) -> GraphMessage:
        graph_message = self.just_load_data()
        
        try:
            graph_builder = GraphBuilder(graph=graph_message)
            graph_builder.build_nodes()
            graph_builder.build_edges()
            return graph_message
        except Exception as e:
            logger.error(f"导入数据到 Neo4j 时出错: {e}")
            exit()
        
    def just_load_data(self) -> GraphMessage:
        try:
            data_loader = DataLoader(self.data_path)
            data_loader.load()
            return data_loader.get_graph()
        except Exception as e:
            logger.error(f"加载数据时出错 {e}")
            exit()
            
    def console_loop(self, graph_message: GraphMessage):
        """
        当数据已经全部被导入到 Neo4j 中, 开始启动
        """
        
        try:
            intention_recognizer = IntentionRecognizer(graph_message, QueryWordCollection())
            cypher_generater = CypherGenerater()
            graph_searcher = GraphSearcher()
            answer_generater = AnswerGenerater()
            
            print("基于知识图谱的问答系统已启动, 请提问: (输入 'exit' 退出)")
            
            while True:
                try:
                    user_input = input("> ")
                    if user_input.lower() == 'exit':
                        break
                    else:
                        answer = self.run(user_input, intention_recognizer, cypher_generater, graph_searcher, answer_generater)
                        logger.info(f"得到的回答: {answer}")
                        print(answer)
                except Exception as e:
                    logger.error(f"输入错误: {e}")
                    print("\n 内部错误, 请重试 \n")
        except Exception as e:
            logger.error(f"启动问答系统时失败 {e}")
    
    def run(self, normal_language_query: str, intention_recognizer: IntentionRecognizer, cypher_generater: CypherGenerater, graph_searcher: GraphSearcher, answer_generater: AnswerGenerater) -> str:
        """
        问答
        """
        
        answers: list[str] = []
        
        intention, entity_map = intention_recognizer.classify(normal_language_question=normal_language_query)
        
        cyphers = cypher_generater.generate(intention, entity_map)
        if len(cyphers) == 0:
            logger.info(f"未生成 Cyher 查询 | 自然语言意图为 {intention} | 自然语言包含的实体为 {entity_map}",)
            return '\n' + answer_generater.no_data_answer + '\n'
        for cypher in cyphers:
            search_result = graph_searcher.search(intention, cypher)
            answer = answer_generater.answer(intention, search_result)
            answers.append(answer)
        
        res = '\n' + '\n'.join(answers) + '\n'
        logger.info(f"提问: {normal_language_query} | 回答: {res}")
        return res

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path', type=str, default="")
    parser.add_argument('--write_to_neo4j', type=str, default="")
    args = parser.parse_args()
    
    cfg = Config()
    
    data_path: str = cfg.test_data_path
    write_to_neo4j: bool = True
    
    if args.data_path == 'all':
        data_path = cfg.data_path
    elif args.data_path == 'test':
        data_path = cfg.test_data_path
    else:
        print(f"错误的参数 --data_path {args.data_path}")
        exit()
        
    if args.write_to_neo4j == 'no':
        write_to_neo4j = False
    elif args.write_to_neo4j == 'yes':
        write_to_neo4j = True
    else:
        print(f"错误的参数 --write_to_neo4j {args.write_to_neo4j}")
        exit()
    
    graphQA = GraphQA(data_path=data_path)
    if write_to_neo4j:
        graph_message = graphQA.import_data_to_neo4j()
        graphQA.console_loop(graph_message)
    else:
        graph_message = graphQA.just_load_data()
        graphQA.console_loop(graph_message)
