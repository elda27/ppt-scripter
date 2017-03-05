from gpt.Presentation import IPresentation
import gpt.NoteText
import zipfile
import sys
import re
import os
import os.path
import locale

class SafePresentation(IPresentation):
	def __init__(self, filename):
		file_pattern = re.compile('ppt/notesSlides/[^/]+?\.xml')
		xml_pattern = re.compile('<.+?>')
	
		notes = list()
		cur_page = 1
		with zipfile.ZipFile(filename, 'r') as ppt:
			for name in ppt.namelist():
				if(file_pattern.match(name)):
					with ppt.open(name) as file:
						texts = file.readlines()
						note = ''.join([xml_pattern.sub('', text.decode('utf-8')) for text in texts]).replace('\n', '')
						notes.append(gpt.NoteText.NoteText(cur_page, note))
					cur_page += 1
		self.NoteTexts = notes
		
	def getNoteTexts(self):
		return self.NoteTexts

	def getPlatformPresentation(self):
		return None

