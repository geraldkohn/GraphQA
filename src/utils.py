import logging
from config import Config

# 初始化标志，默认为 False
initialized = False

logger = logging.getLogger('GraphQA')

def init_logger():
    logger.setLevel(logging.INFO)
    
    log_format = logging.Formatter("[%(asctime)s %(levelname)s %(filename)s:%(lineno)s""] %(message)s")
    
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(log_format)
    # logger.addHandler(console_handler)
    
    cfg = Config()
    
    file_handler = logging.FileHandler(cfg.log_file)
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

if not initialized:
    init_logger()
    initialized = True
