# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import re
import os

from temp.Lightproof import Lightproof


class LightproofChecker:


	def __init__(self):
		# To get errors on LightProof.
		os.environ['PYUNO_LOGLEVEL'] = '1'

		self.L = Lightproof(None, None)

		self.locale = self.L.getLocales()[0]

		s = self.L.getImplementationName()
		self.pkg = s[s.rindex('.') + 1:]

		impl = 'lightproof_impl_' + self.pkg
		self.impl = getattr(__import__('temp.' + impl), impl)

		lng = 'lightproof_' + self.pkg
		self.langrules = getattr(__import__('temp.' + lng), lng)

	def __load_rule(self):
		self.impl.langrule[self.pkg] = self.langrules
		self.impl.compile_rules(self.impl.langrule[self.pkg].dic)

	def compile_rules(self):
		''' Check for bad regular expressions. '''

		errors = []
		position = 1

		for i in self.langrules.dic:
			try:
				i[0] = re.compile(i[0])
			except Exception, e:
				msg = e.message or 'Unknown error.'
				errors.append({'pos' : position, 'msg': msg, 'exp': i[0], 'line': i})

			position += 1

		return errors

	def proofread(self, text):
		''' Assert proofread rules. '''

		if not self.impl.langrule.has_key(self.pkg):
			self.__load_rule()

		nStartOfSentencePos = 0
		nSuggestedSentenceEndPos = len(text)

		ret = self.L.doProofreading(1, text, self.locale, nStartOfSentencePos, nSuggestedSentenceEndPos, ())

		return ret.aErrors

	def word_is_valid(self, word):
		''' Check if the word is valid. '''
		return self.impl.spell(self.locale, word)

	def word_suggestions(self, word):
		''' Get suggestions for the word. '''
		return self.impl.suggest(self.locale, word)

if __name__ == '__main__':

	from temp.Lightproof import Lightproof

	L = LightproofChecker()
	ret = L.proofread('acima citado')
	print (ret)