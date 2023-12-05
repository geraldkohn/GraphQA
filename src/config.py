import os 

class Config:
    def __init__(self):
        self.log_file = os.environ.get("LOG_FILE", 'GraphQA.log')
        self.log_path = os.environ.get("LOG_PATH", "./logs")
        
        self.data_path = os.environ.get('DATA_PATH', './data/medical')
        self.test_data_path = os.environ.get('TEST_DATA_PATH', './data/test')
        
        self.neo4j_host = os.environ.get('NEO4J_HOST', '127.0.0.1')
        self.neo4j_port = os.environ.get('NEO4J_PORT', '7687')
        self.neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')
