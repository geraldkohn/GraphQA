import os 

class Config:
    def __init__(self):
        self.data_path = os.environ.get('DATA_PATH', './data/test')
        self.neo4j_host = os.environ.get('NEO4J_HOST', '127.0.0.1')
        self.neo4j_port = os.environ.get('NEO4J_PORT', '7687')
        self.neo4j_user = os.environ.get('NEO4J_USER', 'neo4j')
        self.neo4j_password = os.environ.get('NEO4J_PASSWORD', 'password')
