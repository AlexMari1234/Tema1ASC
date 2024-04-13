# logger.py
import logging
import time
from logging.handlers import RotatingFileHandler

class AppLogger:
    @staticmethod
    def get_logger(name):
        """ Configurează și returnează un logger pentru o aplicație specifică. """
        # Crează un logger
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)  # Setează nivelul de log la INFO

        # Crează un handler pentru scrierea în fișier, cu rotație
        handler = RotatingFileHandler('webserver.log', maxBytes=20000, backupCount=10)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S UTC')
        handler.setFormatter(formatter)
        
        logging.Formatter.converter = time.gmtime
        # Adaugă handler-ul la logger dacă nu a fost deja adăugat
        if not logger.handlers:
            logger.addHandler(handler)

        return logger
