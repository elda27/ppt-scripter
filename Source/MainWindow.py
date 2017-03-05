# coding:utf-8
import os.path 
from PySide.QtCore import Signal, Slot
from PySide.QtGui import QMainWindow, QWidget,\
  QVBoxLayout, QHBoxLayout,\
  QLabel, QPushButton, QProgressBar, QCheckBox, \
  QListView, QStandardItemModel, QStandardItem,\
  QMessageBox,\
  QDragEnterEvent
import ChooseFileEdit
import gpt
import Logger as private_logger

class MainWindow(QMainWindow):
	def __init__(self, parent = None):
		super().__init__(parent)
		
		self.Logger = private_logger.create('MainWindow.py')
		
		self.Logger.debug('Create MainWindow.')
		self.setAcceptDrops(True)
		self.doLayout()
		self.Logger.debug('Created MainWindow.')

	def dropEvent(self, event):
		self.Logger.debug('Drop down files')
		self.FileListModel.clear()
		source = event.mimeData()
		filepaths = source.urls()
		self.Logger.debug('Drop on %s', filepaths)
		self.FileListModel.appendRow( [QStandardItem(path.toLocalFile()) for path in filepaths] )

	def dragEnterEvent(self, event):
		self.Logger.debug('Came to drop down.')
		mime = event.mimeData()
		if mime.hasUrls():
			self.Logger.debug('Accepted drop down items.')
			event.accept()
		else:
			self.Logger.debug('Rejected drop down items.')
			event.ignore()
		pass

	@Slot()
	def onConvert(self):
		error_files = list()
		index = 0
		while(True):
			item = self.FileListModel.item(index)
			if type(item) is QStandardItem:
				filepath = item.text()
				print(filepath)
				if(filepath == ''):
					continue
				try:
					self.convert(filepath)
				except Exception as e:
					error_files.append(filepath)
					break

			elif item is None or item == 0:
				break

			index += 1
		if(len(error_files) == 0):
			QMessageBox.information(self, self.tr('完了'),	 self.tr('変換が完了しました'))
		else:
			QMessageBox.critical(self, self.tr('エラー'), self.tr('下記のファイルでエラーが発生しました。Safeモードをお試しください。\n' + '\n'.join(error_files)))

	def convert(self, filepath):
		self.Logger.info('Processing {0}.'.format(filepath))

		ppt = None
		if self.SafeModeCheckbox.checkState():
			ppt = gpt.SafePresentation.SafePresentation(filepath)
		else:
			ppt = gpt.Presentation.Presentation(filepath)

		notes = ppt.getNoteTexts()
		filename, ext = os.path.splitext(filepath)
		with open(filename + '.txt', 'w+') as fp:
			for note in notes:
				fp.write('P.{0}\n'.format(note.Page))
				fp.write(note.Text)
				fp.write('\n')

	def doLayout(self):
		central_window = QWidget(self)
		vlayout = QVBoxLayout(central_window)

		self.FileListView = QListView(self)
		self.SafeModeCheckbox = QCheckBox(self.tr('Safeモードで読み込み（エラーが出る場合に使用ください。改行やページ番号等崩れる場合があります。）'), self)
		convert_button = QPushButton(self.tr('変換'), central_window)

		vlayout.addWidget(QLabel(self.tr('ドラッグ&ドロップでファイルを読み込みます'), self))
		vlayout.addWidget(self.FileListView)
		vlayout.addWidget(self.SafeModeCheckbox)
		vlayout.addWidget(convert_button)
		convert_button.clicked.connect(self.onConvert)

		self.FileListModel = QStandardItemModel(self)
		self.FileListModel.setHorizontalHeaderLabels([self.tr('ファイル名')])
		self.FileListView.setModel(self.FileListModel)
		self.FileListView.setAcceptDrops(True)

		self.setCentralWidget(central_window)

