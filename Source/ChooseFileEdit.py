# coding:utf-8

from PySide.QtCore import Signal
from PySide.QtGui import QWidget, QHBoxLayout, QPushButton, QLabel, QLineEdit, QFileDialog

import enum
import functools

class ChooseFileEdit(QWidget):
	class OpenMode(enum.Enum):
		OpenFile = 'OpenFile'
		OpenFiles = 'OpenFiles'
		SaveFile = 'SaveFile'
		OpenDirectory = 'OpenDirectory'

	ShowFileDialogMethodDictionary = {
		'OpenFile':[QFileDialog.getOpenFileName, 'Open file'],
		'OpenFiles':[QFileDialog.getOpenFileNames, 'Open files'],
		'SaveFile':[QFileDialog.getSaveFileName, 'Save file'],
		'OpenDirectory':[QFileDialog.getExistingDirectory, 'Open directory']
		}
	def __init__(self, parent, label, **args):
		super().__init__(parent)
		self.doLayout(label)
		self.initConnection()
		self.Filter = args['filter'] if 'filter' in args else ''
		self.DefaultDirectory = args['defaultdir'] if 'defaultdir' in args else ''
		self.ShowFileDialogMethod = self.dialogFunctionFromOpenMode(args['openmode'])

	def getFilePath():
		return self.PathEdit.getText()

	def dialogFunctionFromOpenMode(self, open_mode):
		if type(open_mode) is str:
			method = ChooseFileEdit.ShowFileDialogMethodDictionary[open_mode]
		elif type(open_mode) is ChooseFileEdit.OpenMode:
			method = ChooseFileEdit.ShowFileDialogMethodDictionary[open_mode.name]
		else:
			raise TypeError()
		return functools.partial(method[0], self, open_mode[1])

	def doLayout(self, label):
		layout = QHBoxLayout(self)
		self.Label = QLabel(label, self)
		self.PathEdit = QLineEdit(self)
		self.LoadButton = QPushButton(self.tr('･･･'), self)
		layout.addWidget(self.Label)
		layout.addWidget(self.PathEdit)
		layout.addWidget(self.LoadButton)

	def initConnection(self):
		self.LoadButton.clicked.connect(self.onLoad)
		self.pathChanged = Signal([str], [list])
		pass

	def onLoad(self):
		path, filter = self.ShowFileDialogMethod(self.DefaultDirectory, self.Filter)
		self.PathEdit.setText(path)
		if not path is None:
			self.pathChanged.emit(path)
		pass
