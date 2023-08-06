import logging
import logging.handlers


def init_log(log_name='simple_operation', log_level=logging.DEBUG):
    """
    init module log
    :param log_name:
    :return:
    """
    logger = logging.getLogger(name=log_name)
    formatter = logging.Formatter('[%(asctime)s][%(levelname)s]: %(message)s')
    hdlr = logging.StreamHandler()
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(log_level)
    return logger


simple_operation_log = init_log()
