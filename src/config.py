
# !python 3.6
# -*-coding: utf-8 -*-

import logging


# =========================================== #
# -----------------  日志  ------------------ #
# =========================================== #
'''
    ## 使用方法
        - 在需要记录日志的地方引入全局变量"VIEW_LOG"
'''

log_level = logging.INFO
LOG = logging.getLogger('client')
LOG.setLevel(log_level)
FORMAT = logging.Formatter('%(asctime)-15s %(module)s.%(funcName)s[%(lineno)d] %(levelname)s %(message)s')
sh = logging.StreamHandler()
sh.setFormatter(FORMAT)
sh.setLevel(log_level)
fh = logging.FileHandler('./client.log', mode='a', encoding='utf-8')
fh.setFormatter(FORMAT)
fh.setLevel(log_level)
LOG.addHandler(sh)
LOG.addHandler(fh)


# 数据库路径
DB_DATA_PATH = ".\data_client.db"

# 数据库时间字段的默认无效时间
DEFAULT_TIME = -123.456
