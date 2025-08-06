import logging
from datetime import datetime
from typing import Any

class Logger:
    def __init__(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger(__name__)
    
    def info(self, message: str, data: Any = None):
        if data:
            self.logger.info(f"{message}: {data}")
        else:
            self.logger.info(message)
    
    def error(self, message: str, error: Any = None):
        if error:
            self.logger.error(f"{message}: {error}")
        else:
            self.logger.error(message)
    
    def warn(self, message: str, data: Any = None):
        if data:
            self.logger.warn(f"{message}: {data}")
        else:
            self.logger.warn(message)
    
    def warning(self, message: str, data: Any = None):
        if data:
            self.logger.warning(f"{message}: {data}")
        else:
            self.logger.warning(message)
    
    def debug(self, message: str, data: Any = None):
        if data:
            self.logger.debug(f"{message}: {data}")
        else:
            self.logger.debug(message)

logger = Logger()