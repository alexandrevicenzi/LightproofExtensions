# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import re

from Lightproof import Lightproof


class LightproofChecker:

	def __init__(self):
		self.L = Lightproof(None, None)
		s = L.getImplementationName()
		self.pkg = s[s.rindex('.') + 1:] 
		self.langrules = __import__('lightproof_' + self.pkg)

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
		'''  '''
		
		locale = L.getLocales()[0]
		nStartOfSentencePos = 0
		nSuggestedSentenceEndPos = len(text)

		ret = L.doProofreading(1, text, locale, nStartOfSentencePos, nSuggestedSentenceEndPos, ())

		return ret.aErrors

class LightproofCheckerCmd(LightproofChecker):

	def __init__(self):
		LightproofChecker.__init__(self)

class LightproofCheckerGui(LightproofChecker):

	def __init__(self):
		LightproofChecker.__init__(self)