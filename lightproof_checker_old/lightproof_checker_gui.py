# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os

from extensions import unpack_oxt, create_init_file
from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow
from threading import Thread

def select_file(msg="Please choose a file", gtk_action=Gtk.FileChooserAction.OPEN, filter=None):
	dialog = Gtk.FileChooserDialog(msg, 
								   action=gtk_action,
								   buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))

	dialog.set_default_size(600, 400)

	response = dialog.run()

	filename = None

	if response == Gtk.ResponseType.OK:
		filename = dialog.get_filename()

	dialog.destroy()

	return filename

def thread_safe(func):

	def callback(*args):
		GObject.idle_add(func, *args)

	return callback

class LightproofWindow(GladeWindow):


	def __init__(self):
		GladeWindow.__init__(self, 'window.glade', 'main')
		self.w.show({'rb_compile': True})

	def on_btn_oxt_open_clicked(self, *args):
		self.w.oxt_filename.set_text(select_file() or '')

	def on_btn_test_open_clicked(self, *args):
		self.w.test_filename.set_text(select_file() or '')

	def on_btn_run_clicked(self, *args):

		self.w.results.get_buffer().set_text('')

		w = self.w.get()

		oxt = w['oxt_filename']

		if not oxt:
			self.append_text('No file specified.\nYou must select an OXT file.\nAborted.')
			self.w.oxt_filename.grab_focus()
			return

		test = w['test_filename']

		if w['rb_test'] or w['rb_both']:
			if not test:
				self.append_text('No file specified.\nYou must select a test file.\nAborted.')
				self.w.test_filename.grab_focus()
				return

		t = Thread(target=self.run, args=(oxt, test, w,))
		t.daemon = True
		t.start()

	def run(self, oxt, test, w):

		def compile_rules():
			self.append_text('Compiling...')

			ret = L.compile_rules()

			if len(ret) > 0:
				for e in ret:
					msg = '%s at position %d.\nExpression: %s\nLine: %s'\
						% (e['msg'], e['pos'], e['exp'], e['line'])
					self.append_text(msg)
			else:
				self.append_text('Success.')

		def do_proofread():
			pass

		try:
			if os.path.exists('temp'):
				import shutil
				shutil.rmtree('temp')

			os.makedirs('temp')
			create_init_file('temp')

			self.append_text('Unpackin OXT file "%s" ...' % oxt)

			if not unpack_oxt(oxt, 'temp'):
				self.append_text('Invalid OXT file "%s".\nAborted.' % oxt)
				return

			self.append_text('Unpacked.')

			from lightproof_checker import LightproofChecker

			L = LightproofChecker()

			if w['rb_compile']:
				compile_rules()

			elif w['rb_test']:
				do_proofread()

			elif w['rb_both']:
				compile_rules()
				do_proofread()

			else:
				self.append_text('Unsupported option.\nAborted.')

		except Exception, e:
			self.append_text(e.message)

	def on_close(self, *args):
		self.close()
		Gtk.main_quit()

	@thread_safe
	def append_text(self, text):
		self.w.results.get_buffer().insert(self.w.results.get_buffer().get_end_iter(), text + "\n")


if __name__ == "__main__":

	Win = LightproofWindow()
	Win.show()

	Gtk.main()