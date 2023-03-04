import logging

class Logger:
    
    def __init__(self):
        logging.basicConfig('%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR, filename='log.txt')
        self.log = logging.getLogger(__name__)

    @property
    def logger(self):
        return self.log