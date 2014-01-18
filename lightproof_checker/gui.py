# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os
import re

from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow
from threading import Thread


def thread_safe(func):

	def callback(*args):
		GObject.idle_add(func, *args)

	return callback


class LightProofGui(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'gui.glade', 'main')

	def on_main_show(self, *args):
		self.load_state()

	def on_context_toggled(self, *args):


		def configure(lo):
			if (lo):
				self.w.input_f.show()
				self.w.oxt_pkg_f.show()

				self.w.integrity.hide()
				self.w.compile.hide()

				self.w.spell.show()
				self.w.grammar.show()

				self.w.locale_f.show()
				self.w.input_fr.show()
			else:
				self.w.input_f.hide()
				self.w.oxt_pkg_f.hide()

				self.w.integrity.show()
				self.w.compile.show()

				self.w.spell.hide()
				self.w.grammar.hide()

				self.w.locale_f.hide()
				self.w.input_fr.hide()
			

		w = self.w.get()

		if w['libreoffice']:
			configure(True)

			if w['compile'] or w['integrity']:
				self.w.show({'spell' : True})

		elif w['standalone']:
			configure(False)

			if w['spell'] or w['grammar']:
				self.w.show({'integrity' : True})
		else:
			pass

	def on_input_toggled(self, *args):

		w = self.w.get()

		self.w.hbox_file.hide()
		self.w.sw_text.hide()
		self.w.input_url.hide()
		self.w.input_fr.set_vexpand(False)

		if w['file']:
			self.w.hbox_file.show()

		elif w['text']:
			self.w.sw_text.show()
			self.w.input_fr.set_vexpand(True)

		elif w['url']:
			self.w.input_url.show()

		else:
			pass

	def on_close(self, *args):
		self.save_state()
		self.close()
		Gtk.main_quit()

	def on_bt_execute_clicked(self, *args):

		self.w.results.get_buffer().set_text('')

		w = self.w.get()

		t = Thread(target=self.execute, args=(w,))
		t.daemon = True
		t.start()

	def execute(self, w):
		
		if w['libreoffice']:

			lang = w['locale']

			if not lang:
				self.append_result('Locale is required.')
				return

			self.append_result('Starting LibreOffice...')

			from bridge import LightProofBridge

			self.bridge = LightProofBridge(lang=lang, error_func=self.append_result)


			if w['file']:
				if not os.path.exists(w['file']):
					self.append_result('File not found: ' + w['file'])
					return

				with open(w['input_file']) as f:
					text = f.read

			elif w['text']:
				text = w['input_text']

			elif w['url']:
				text = ''

			else:
				text = ''

			if w['spell']:

				self.append_result('Starting Spell Checker...')
				self.append_result('Locale: ' + lang)
				self.append_result('Text: ' + text)

				self.spell_check(text)

			elif w['grammar']:

				self.append_result('Starting Grammar Checker...')
				self.append_result('Locale: ' + lang)

				self.grammar_check(text)

			else:
				pass

	def spell_check(self, text):
		text = unicode(text, "utf-8")

		for word in re.findall(r"[\w']+", text, re.UNICODE):
			sug = self.bridge.spell(word)

			if sug:
				self.append_result('%s: Not in dictionary. Suggestion: %s' % (word, ', '.join(sug)))
			else:
				self.append_result('%s: In dictionary.' % (word))

	def grammar_check(self, text):

		ret = self.bridge.proofread(text)
		print(ret)
		self.append_result(ret)

	@thread_safe
	def append_result(self, text):
		self.w.results.get_buffer().insert(self.w.results.get_buffer().get_end_iter(), text + "\n")

	def save_state(self):
		pass

	def load_state(self):

		self.w.show({'libreoffice' : True, 
					 'spell' : True, 
					 'file' : True, 
					 'manual' : True, 
					 'locale' : 'pt_BR',
					 'input_text' : 'não  da  assim , pois.',
					})

		if not os.path.exists('gui.state'):
			return

		with open('gui.state', 'r') as f:
			lines = f.readlines()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()
