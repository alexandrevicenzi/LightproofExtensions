# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os
import time
import uno

from com.sun.star.lang import Locale 

class LightProofBridge:


	def __init__(self, soffice_path='soffice'):
		self.soffice = soffice_path

		self.local_ctx = uno.getComponentContext()

		resolver = self.local_ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', self.local_ctx)

		load = False

		while not load:
			try:
				self.soffice_ctx = resolver.resolve( "uno:pipe,name=addtemppipe;urp;StarOffice.ComponentContext" )
				load = True
			except:
				os.system(self.soffice + ' --accept="pipe,name=addtemppipe;urp;StarOffice.ServiceManager" --headless --nologo --nofirststartwizard &')
				time.sleep(4)

		smgr = self.soffice_ctx.ServiceManager

		self.spellchecker = smgr.createInstanceWithContext("com.sun.star.linguistic2.SpellChecker", self.local_ctx)
		self.grammar_checker = None

	def is_valid_word(self, word, lang):

		loc = Locale(lang[0:2], lang[3:5], "")

		return self.spellchecker.isValid(word, loc, ())

	def spell(self, word, lang):

		loc = Locale(lang[0:2], lang[3:5], "")
		sug = self.spellchecker.spell(word, loc, ())
		
		if sug:
			return sug.getAlternatives()
		else:
			return []

if __name__ == '__main__':
	B = LightProofBridge()

	if not B.is_valid_word('nao', 'pt_BR'):
		print('Suggestions:')
		print(B.spell('nao', 'pt_BR'))
	else:
		print('Word is OK.')
