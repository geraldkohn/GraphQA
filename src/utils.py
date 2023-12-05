import logging
import os

from config import Config

# 初始化标志，默认为 False
initialized = False

logger = logging.getLogger('GraphQA')

def init_logger():
    cfg = Config()
    
    if not os.path.exists(cfg.log_path):
        os.makedirs(cfg.log_path)
    
    logger.setLevel(logging.INFO)
    
    log_format = logging.Formatter("[%(asctime)s %(levelname)s %(filename)s:%(lineno)s""] %(message)s")
    
    # console_handler = logging.StreamHandler()
    # console_handler.setFormatter(log_format)
    # logger.addHandler(console_handler)
    
    file_handler = logging.FileHandler(os.path.join(cfg.log_path, cfg.log_file))
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

if not initialized:
    init_logger()
    initialized = True
