"""logger utility module"""
import logging
import logging.config
from datetime import datetime
import os
from colorlog import ColoredFormatter


def get_logger_instance(level='', logger_name='defaultLogger'):
    """Creates the logger object"""
    log_obj = LogClass()
    logger = log_obj.get_logger(level=level, logger_name=logger_name)
    return logger


def create_directory(name):
    """Checks if the directory exists and creates if not"""
    if not os.path.exists(name):
        os.makedirs(name)


def generate_log_file_path(log_folder_path):
    """
    Creates the path of the log file as per current date
    :param log_folder_path:
    :return: returns a string containing the log file path
    """
    date = datetime.now().strftime("_%d_%m_%Y")
    log_file_name = "".join(['logfile', date, '.log'])
    log_file_path = os.path.join(log_folder_path, log_file_name)
    log_file_path = log_file_path.replace('\\', '\\\\')
    return log_file_path


class LogClass:
    """Logger class"""
    def __init__(self):
        """Initialise the logger configuration
           Read the configuration from 'logger.conf' file
        """
        log_folder_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                                       'logs')
        create_directory(log_folder_path)
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logger.conf')
        log_file_name = generate_log_file_path(log_folder_path)
        logging.config.fileConfig(path, defaults={'logfilename': r"".join([log_file_name, ""])})

    def get_logger(self, level='', logger_name='defaultLogger'):
        """returns the logger object"""
        # mention the name of the logger according to the requirement
        # refer logger.conf file for the different loggers configured
        logger = logging.getLogger(logger_name)
        if level != '':
            level = level.strip().lower()
            if level == 'debug':
                logger.setLevel(logging.DEBUG)
            elif level == 'info':
                logger.setLevel(logging.INFO)
            elif level == 'warning':
                logger.setLevel(logging.WARNING)
            elif level == 'error':
                logger.setLevel(logging.ERROR)
            elif level == 'critical':
                logger.setLevel(logging.CRITICAL)

        return logger
