# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow

class LightProofGui(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'gui.glade', 'main')

	def on_main_show(self, *args):
		self.w.show({'rb_libreoffice' : True, 'rb_spell' : True, 'rb_file' : True})

	def on_context_toggled(self, *args):

		w = self.w.get()

		if w['rb_libreoffice']:
			self.w.rb_compile.set_sensitive(False)
			self.w.rb_spell.set_sensitive(True)
			self.w.rb_grammar.set_sensitive(True)
			self.w.rb_text.set_sensitive(True)

			if w['rb_compile']:
				self.w.show({'rb_spell' : True})

		elif w['rb_standalone']:
			self.w.rb_compile.set_sensitive(True)
			self.w.rb_spell.set_sensitive(False)
			self.w.rb_grammar.set_sensitive(False)
			self.w.rb_text.set_sensitive(False)

			self.w.show({'rb_compile' : True})

			if w['rb_text']:
				self.w.show({'rb_file' : True})
		else:
			pass

	def on_input_toggled(self, *args):

		w = self.w.get()

		self.w.al_text.hide()
		self.w.al_file.hide()
		self.w.bt_file.hide()

		if w['rb_file']:
			self.w.al_file.show()
			self.w.bt_file.show()

		elif w['rb_text']:
			self.w.al_text.show()

		elif w['rb_url']:
			self.w.al_file.show()

		else:
			pass

	def on_close(self, *args):
		self.close()
		Gtk.main_quit()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()
