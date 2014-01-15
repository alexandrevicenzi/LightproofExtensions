# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os

from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow


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

	def save_state(self):
		pass

	def load_state(self):

		if not os.path.exists('gui.state'):
			self.w.show({ 'libreoffice' : True, 'spell' : True, 'file' : True, 'manual' : True, })

		with open('gui.state', 'r') as f:
			lines = f.readlines()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()
