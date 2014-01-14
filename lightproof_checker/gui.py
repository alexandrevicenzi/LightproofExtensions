# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow

class LightProofGui(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'gui.glade', 'main')

	def on_close(self, *args):
		self.close()
		Gtk.main_quit()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()