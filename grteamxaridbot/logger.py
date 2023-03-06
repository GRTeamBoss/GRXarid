import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.ERROR, filename='./../log.txt')
log = logging.getLogger(__name__)