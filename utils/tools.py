#!/user/bin/even Python3
# -*- coding:utf-8 -*-
# tools.py
# 日常工具类
# author:zhaohexin
# time：2020/4/1 10:43
import logging
import os

# 启动日志
logger = logging.getLogger('log')


def create_dir(dir_path):
    """
    创建文件夹
    :param dir_path:文件夹路径
    :return: 返回成功与否
    """
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        return True
    except Exception as e:
        logger.error(e)
        return False
