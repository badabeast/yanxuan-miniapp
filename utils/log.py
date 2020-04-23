import logging
import os
from time import strftime
import sys



cur_path = os.path.dirname(os.path.abspath(__file__))
log_path = os.path.join(os.path.dirname(cur_path), 'logs')

if not os.path.exists(log_path):os.mkdir(log_path)

class Log(object):
    def __init__(self):
        self.logname = os.path.join(log_path, '%s.log' % strftime('%Y-%m-%d'))
        self.errorlogname = os.path.join(log_path, '%s.error.log' % strftime('%Y-%m-%d'))
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.DEBUG)
        # 日志输出格式
        self.formatter = logging.Formatter('[%(asctime)s] - %(filename)s] - %(levelname)s: %(message)s')

    def __console(self, level, message):
        # 创建一个FileHandler，用于写到本地
        fh = logging.FileHandler(self.logname, 'a', encoding='utf-8')  # 这个是python3的
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(self.formatter)
        self.logger.addHandler(fh)
        
        # 错误日志
        feh = logging.FileHandler(self.errorlogname, 'a', encoding='utf-8')  # 这个是python3的
        feh.setLevel(logging.ERROR)
        feh.setFormatter(self.formatter)
        self.logger.addHandler(feh)

        # 创建一个StreamHandler,用于输出到控制台
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        ch.setFormatter(self.formatter)
        self.logger.addHandler(ch)

        if level == 'info':
            self.logger.info(message)
        elif level == 'debug':
            self.logger.debug(message)
        elif level == 'warning':
            self.logger.warning(message)
        elif level == 'error':
            self.logger.error(message)
        # 避免日志输出重复
        self.logger.removeHandler(ch)
        self.logger.removeHandler(fh)
        self.logger.removeHandler(feh)
        # 关闭打开的文件
        fh.close()
        feh.close()


    def debug(self,message):
        self.__console('debug', message)

    def info(self, message):
        self.__console('info', message)

    def warning(self, message):
        self.__console('warning', message)

    def error(self, message):
        self.__console('error', message)