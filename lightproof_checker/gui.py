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


		def configure(b):
			self.w.input_f.set_sensitive(b)
			self.w.oxt_pkg_f.set_sensitive(b)

			self.w.integrity.set_sensitive(not b)
			self.w.compile.set_sensitive(not b)
			self.w.spell.set_sensitive(b)
			self.w.grammar.set_sensitive(b)

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

				with open(w['file']) as f:
					text = f.read

			elif w['text']:
				text = 'nao foi dess ves, mano.'

			elif w['url']:
				text = ''

			else:
				text = ''


			if w['spell']:

				self.append_result('Starting Spell Checker...')
				self.append_result('Locale: ' + lang)

				self.spell_check(text)

			elif w['grammar']:

				self.append_result('Starting Grammar Checker...')
				self.append_result('Locale: ' + lang)

				self.grammar_check(text)

			else:
				pass

	def spell_check(self, text):

		for word in re.findall(r"[\w']+", text):
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

		self.w.show({ 'libreoffice' : True, 'spell' : True, 'file' : True, 'manual' : True, })

		if not os.path.exists('gui.state'):
			return

		with open('gui.state', 'r') as f:
			lines = f.readlines()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()
