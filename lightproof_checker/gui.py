# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow

class LightProofGui(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'gui.glade', 'main')

	def on_main_show(self, *args):
		self.load_state()

	def on_context_toggled(self, *args):

		w = self.w.get()

		if w['libreoffice']:
			self.w.compile.set_sensitive(False)
			self.w.spell.set_sensitive(True)
			self.w.grammar.set_sensitive(True)
			self.w.text.set_sensitive(True)
			self.w.oxt_pkg_f.set_sensitive(True)

			if w['compile']:
				self.w.show({'spell' : True})

		elif w['standalone']:
			self.w.compile.set_sensitive(True)
			self.w.spell.set_sensitive(False)
			self.w.grammar.set_sensitive(False)
			self.w.text.set_sensitive(False)
			self.w.oxt_pkg_f.set_sensitive(False)

			self.w.show({'compile' : True})

			if w['text']:
				self.w.show({'file' : True})
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
		self.w.show({ 'libreoffice' : True, 'spell' : True, 'file' : True, 'manual' : True, })

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()
