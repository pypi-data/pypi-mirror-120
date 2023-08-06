import logging
import logging.handlers
import os

def my_logger(module_name, log_file):
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.DEBUG)

    # Create handlers
    # os.path.join(os.path.dirname(os.path.realpath(__file__))
    c_handler = logging.StreamHandler()
    f_handler = logging.handlers.RotatingFileHandler(filename=os.path.join(os.path.dirname(os.path.realpath("logs/")), "logs/"+log_file))
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add it to handlers
    c_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    f_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(lineno)d - %(message)s')
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    return logger
#
# logger = my_logger(__name__)
# logger.warning('This is a warning')
# logger.error('This is an error')
# logger.info('This is an info')
# logger.debug('This is an debug')