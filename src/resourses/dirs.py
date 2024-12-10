# coding=utf-8
"""
Модуль предоставляет константы, содержащие имена каталогов с ресурсами
"""

from os import path

RES_DIR = path.dirname(__file__)
LOG_FILE = path.join(RES_DIR, 'log_viewer.log')
CFG_FILE = path.join(RES_DIR, 'log_viewer.cfg')

