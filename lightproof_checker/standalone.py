# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import re
import os
import uno

from temp.Lightproof import Lightproof


class LightproofStandalone:


	def __init__(self):
		pass

	def load_package(self):
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

	def check_pkg(self):
		pass

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

		if not self.impl.langrule.has_key(self.pkg):
			self.__load_rule()

		nStartOfSentencePos = 0
		nSuggestedSentenceEndPos = len(text)

		ret = self.L.doProofreading(1, text, self.locale, nStartOfSentencePos, nSuggestedSentenceEndPos, ())

		return ret.aErrors

if __name__ == '__main__':

	from temp.Lightproof import Lightproof

	L = LightproofChecker()

	print(L.compile_rules())
	
	ret = L.proofread('acima citado')
	print (ret)
