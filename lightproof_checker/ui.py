# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os
import re

from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow, thread_safe
from threading import Thread


class LightProofGui(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'ui.glade', 'configuration')

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
				self.w.oxt_file_f.hide()
				self.w.lo_box_op.show()
				self.w.lo_box_op.set_vexpand(True)

			else:
				self.w.input_f.hide()
				self.w.oxt_pkg_f.hide()
				self.w.integrity.show()
				self.w.compile.show()
				self.w.spell.hide()
				self.w.grammar.hide()
				self.w.oxt_file_f.show()
				self.w.lo_box_op.hide()
				self.w.lo_box_op.set_vexpand(False)
			

		w = self.w.get()

		if w['libreoffice']:
			configure(True)

			if not w['both_opt']:
				self.w.show({'both_opt' : True})

		elif w['standalone']:
			configure(False)

			if not w['both_opt']:
				self.w.show({'both_opt' : True})
		else:
			pass

	def on_input_toggled(self, *args):

		w = self.w.get()

		self.w.hbox_file.hide()
		self.w.sw_text.hide()
		self.w.input_url.hide()

		if w['file']:
			self.w.hbox_file.show()
		elif w['text']:
			self.w.sw_text.show()
		elif w['url']:
			self.w.input_url.show()
		else:
			pass

	def on_oxt_pkg_toggled(self, *args):

		w = self.w.get()

		if w['manual']:
			self.w.oxt_file_f.hide()
		elif w['deploy']:
			self.w.oxt_file_f.show()
		else:
			pass
		

	def on_close(self, *args):
		self.save_state()
		self.close()
		Gtk.main_quit()

	def on_bt_execute_clicked(self, *args):
		R = ResultsGui()
		R.show()

	def save_state(self):
		pass

	def load_state(self):

		self.w.show({'libreoffice' : True, 
					 'spell' : True, 
					 'unit_test' : True,
					 'file' : True, 
					 'manual' : True, 
					})

		if not os.path.exists('gui.state'):
			return

		with open('gui.state', 'r') as f:
			lines = f.readlines()

class ResultsGui(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'ui.glade', 'results')

	def run(self, func):
		pass

	def update_status(self, str):
		pass

	def on_bt_close_clicked(self, *args):
		self.close()

	def on_results_delete_event(self, *args):
		self.close()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()
