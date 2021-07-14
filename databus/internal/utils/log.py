# -*- coding: utf-8 -*-
import logging.config
import os
import sys
import time
from logging.handlers import TimedRotatingFileHandler

import rich.traceback
import simplejson as json
from pythonjsonlogger import jsonlogger
from rich.logging import RichHandler

rich.traceback.install()
path = sys.path[0]
# 存放log文件的路径
log_path = os.path.join(path)
log_file_name = time.strftime("%Y-%m-%d", time.gmtime()) + '.log'
LOG_FILE = os.path.join(log_path, log_file_name)
LOG_LV = logging.INFO
# https://docs.python.org/2/library/logging.html#logrecord-attributes
simple_fmt = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s : %(message)s"
thread_fmt = "%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - %(lineno)s - %(threadName)s : %(message)s"
json_formatter = jsonlogger.JsonFormatter(simple_fmt,
                                          json_indent=4,
                                          json_encoder=json.JSONEncoder,
                                          json_ensure_ascii=False)
simple_formatter = logging.Formatter(simple_fmt)
thread_formatter = logging.Formatter(thread_fmt)

# json日志的handler
json_console_handler = logging.StreamHandler()
json_console_handler.setFormatter(json_formatter)
json_console_handler.setLevel(LOG_LV)
json_file_handler = TimedRotatingFileHandler(LOG_FILE, when='midnight')
json_file_handler.setFormatter(json_formatter)
json_file_handler.setLevel(LOG_LV)

# 非json日志handler
basic_console_handler = logging.StreamHandler()
basic_console_handler.setFormatter(simple_formatter)
basic_file_handler = TimedRotatingFileHandler(LOG_FILE, when="midnight")
basic_file_handler.setFormatter(thread_formatter)

# 日志默认配置
logging.config.dictConfig({"disable_existing_loggers": False, "version": 1})
# logging.root.handlers = [json_console_handler, json_file_handler]  # 默认会添加一个默认的handler,需要移除
# logging.root.setLevel(LOG_LV)
logging.basicConfig(level=LOG_LV,
                    format="%(message)s",
                    datefmt="[%Y-%m-%d %H:%M:%S]",
                    handlers=[RichHandler(rich_tracebacks=True)])
logging.getLogger("requests").setLevel(LOG_LV)


def handle_uncaught_exception(exctype, value, traceback):
    if issubclass(exctype, KeyboardInterrupt):
        sys.__excepthook__(exctype, value, traceback)
        return
    logging.root.error("Uncaught exception", exc_info=(exctype, value, traceback))


def disable_json_format_log():
    '''关闭json格式的日志'''
    logging.root.removeHandler(json_console_handler)
    logging.root.removeHandler(json_file_handler)
    logging.root.addHandler(basic_console_handler)
    logging.root.addHandler(basic_file_handler)


def enable_json_format_log():
    '''开启json格式的日志'''
    logging.root.removeHandler(basic_console_handler)
    logging.root.removeHandler(basic_file_handler)
    logging.root.addHandler(json_file_handler)
    logging.root.addHandler(json_console_handler)


# disable_json_format_log()
LOGGER = logging.getLogger(__name__)
