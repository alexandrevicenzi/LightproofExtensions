# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

from extensions import unpack_oxt
from gi.repository import Gtk
from gladebuilder import GladeWindow


def select_file(msg="Please choose a file", gtk_action=Gtk.FileChooserAction.OPEN, filter=None):
	dialog = Gtk.FileChooserDialog(msg, 
								   action=gtk_action,
								   buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, "Select", Gtk.ResponseType.OK))

	dialog.set_default_size(800, 400)

	response = dialog.run()

	filename = None

	if response == Gtk.ResponseType.OK:
		filename = dialog.get_filename()

	dialog.destroy()

	return filename

class LightproofWindow(GladeWindow):


	def __init__(self):
		GladeWindow.__init__(self, 'interface.glade', 'main')
		self.w.show({'rb_compile': True})

	def on_btn_oxt_open_clicked(self, *args):
		self.w.oxt_filename.set_text(select_file() or '')

	def on_btn_test_open_clicked(self, *args):
		self.w.test_filename.set_text(select_file() or '')

	def on_btn_run_clicked(self, *args):
		
		self.w.results.get_buffer().set_text('')

		oxt = self.w.oxt_filename.get_text()

		if not oxt:
			self.append_text('Invalid OXT file.\nAborted.')
			return


		self.append_text('Unpackin OXT file "%s" ...' % oxt)
		self.append_text('Unpacked.')

	def on_close(self, *args):
		self.close()
		Gtk.main_quit()

	def append_text(self, text):
		self.w.results.get_buffer().insert(self.w.results.get_buffer().get_end_iter(), text + "\n")


if __name__ == "__main__":

	Win = LightproofWindow()
	Win.show()

	Gtk.main()