# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)
# Thanks to Laszlo Nemeth.

import os
import time
import uno

from com.sun.star.lang import Locale 

class LightProofBridge:


	def __init__(self, lang, soffice_path='soffice'):

		self.locale = Locale(lang[0:2], lang[3:5], '')
		self.soffice_path = soffice_path
		self.local_ctx = uno.getComponentContext()

		self.__load_soffice_ctx()

		smgr = self.soffice_ctx.ServiceManager

		self.spell_checker = smgr.createInstanceWithContext('com.sun.star.linguistic2.SpellChecker', self.local_ctx)
		self.grammar_checker = smgr.createInstanceWithContext('org.libreoffice.comp.pyuno.Lightproof.' + lang, self.local_ctx)

	def __del__(self):
		# FIX-ME
		# Binary URP bridge already disposed.
		os.system('killall soffice.bin')

	def __load_soffice_ctx(self):

		resolver = self.local_ctx.ServiceManager.createInstanceWithContext('com.sun.star.bridge.UnoUrlResolver', self.local_ctx)

		load = False

		while not load:
			try:
				self.soffice_ctx = resolver.resolve('uno:pipe,name=addtemppipe;urp;StarOffice.ComponentContext')
				load = True
			except:
				os.system('%s --accept="pipe,name=addtemppipe;urp;StarOffice.ServiceManager" --headless --nologo --nofirststartwizard &' %\
					self.soffice_path)
				time.sleep(4)

	def is_valid_word(self, word):
		return self.spell_checker.isValid(word, self.locale, ())

	def spell(self, word):
		sug = self.spell_checker.spell(word, self.locale, ())

		if sug:
			return sug.getAlternatives()
		else:
			return []

	def proofread(self, text):
		return self.grammar_checker.doProofreading(1, text, self.locale, 0, len(text), ())

if __name__ == '__main__':

	B = LightProofBridge('pt_BR')

	if not B.is_valid_word('nao'):
		print('Suggestions:')
		print(B.spell('nao'))
	else:
		print('Word is OK.')

	ret = B.proofread('Este  é um novo caso , eu acho')
	print(ret.aErrors)
	print(ret.aText)
