import logging
from .config import configuration

logging.basicConfig(level=configuration.log_level,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename=configuration.log_file,
                filemode='w')

logger = logging

def ErrorLog(func):
    def _dec(*args, **kwargs):
        try:
            func(*args, **kwargs)
        except Exception as e:
            logger.error("An error has occurr in the {func}, error:{e}".format(**locals()))
            raise e
    return _dec