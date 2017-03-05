# coding:utf-8
from logging import getLogger, StreamHandler, FileHandler, Formatter, DEBUG, INFO, ERROR, CRITICAL
import sys
import os
import os.path
import Configuration as config
from datetime import datetime

Level = DEBUG
Filename = datetime.now().strftime('%Y-%m-%d\'%H-%M-%S') + '.txt'

def create(importfile):
	global Filename
	global Level
	level = Level
	logger = getLogger(importfile)
	logger.setLevel(level)

	formatter = Formatter('[%(levelname)s, %(asctime)s, %(name)s]: %(message)s')
	handler = StreamHandler()
	handler.setLevel(level)
	handler.setFormatter(formatter)

	os_dir = ''
	if sys.platform == 'win32':
		os_dir = os.path.join(os.environ.get('APPDATA'), config.ApplicationName)
	else:
		os_dir = os.path.join(os.environ.get('HOME'), '.' + config.ApplicationName)
	
	if not os.path.exists(os_dir):
		os.mkdir(os_dir)

	filename = os.path.join(os_dir, Filename)

	file_handler = FileHandler(filename)
	file_handler.setLevel(level)
	file_handler.setFormatter(formatter)

	logger.addHandler(handler)
	logger.addHandler(file_handler)

	return logger

