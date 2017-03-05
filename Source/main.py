# coding:utf-8

import pptx
import sys
import io
import argparse
import logging
import gpt

import Logger

import MainWindow
import Language
from PySide.QtCore import QTextCodec, QTranslator
from PySide.QtGui import QApplication

def main(argv):
	QTextCodec.setCodecForTr(QTextCodec.codecForName('utf-8'))

	parsed_args = parseArguments(argv)
	logger = createLogger(parsed_args.IsDebugging)

	logger.debug('Create application.')
	app = QApplication(argv)
	if hasattr(parsed_args, 'Language') and not parsed_args.Language is None:
		translator = createTranslator(parsed_args.Language)
		app.installTranslator(translator)

	window = MainWindow.MainWindow()

	logger.debug('Check to execute a CUI mode.')
	if(parsed_args.InputFiles):
		logger.debug('Enter the CUI mdoe.')

		for file in parsed_args.InputFiles:
			try:
				window.convert(file)
			except e as Exception:
				logger.error('Failed to conversion %s', file)
				logger.debug(e)

		logger.info('Finished to convert all files.')
		return

	logger.debug('Enter the GUI mode.')
	window.show()
	sys.exit(app.exec_())

def parseArguments(argv):
	if argv[0] == 'python':
		args = argv[2:]
	else:
		args = argv[1:]

	parser = argparse.ArgumentParser('Convert pptx to text files')
	parser.add_argument('-i', '--input', nargs='*', type=str, required=False, dest='InputFiles', help='Input files.')
	parser.add_argument(
		'--debug', action='store_true', 
		required=False, dest='IsDebugging', 
		help='Output debug log.'
		)
	#parser.add_argument('--lang', nargs=1, action='store', type=str, dest='Language', help='Language')
	parsed_args = parser.parse_args(args)

	return parsed_args

def createLogger(is_debug):
	if(is_debug):
		Logger.Level = logging.DEBUG
	else:
		Logger.Level = logging.INFO

	logger = Logger.create('main.py')
	return logger

def createTranslator(language):
	translator = QTranslator()
	translator.load('local/' + Language.Language(language).name())
	return translator

if __name__ == '__main__':
	main(sys.argv)
