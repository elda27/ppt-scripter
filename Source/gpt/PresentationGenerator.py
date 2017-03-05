from gpt import Presentation, SafePresentation
from enum import Enum

class PresentationGenerator:
	class PresentationMode(Enum):
		Normal = 0
		SafeMode = 1
		Default = Normal

	def __init__():
		self.Mode = self.Presentation.Default

	def setSafeMode():
		self.Mode = self.PresentationMode.SafeMode

	def generate(filename):
		if(self.Mode == self.PresentationMode.Normal):
			return Presentation(filename)
		elif(self.Mode == self.PresentationMode.SafeMode):
			return SafePresentation(filename)
		else:
			raise ValueError()
