import logging
import time
from logging.handlers import RotatingFileHandler

class AppLogger:
    @staticmethod
    def get_logger(name):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        handler = RotatingFileHandler('webserver.log', maxBytes=20000, backupCount=10)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S UTC')
        handler.setFormatter(formatter)
        logging.Formatter.converter = time.gmtime
        if not logger.handlers:
            logger.addHandler(handler)

        return logger
