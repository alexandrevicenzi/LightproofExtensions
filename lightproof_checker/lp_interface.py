# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

from gi.repository import Gtk
from gladebuilder import GladeWindow


class LPInterdace(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'interface.glade', 'main')

	def on_close(self, *args):
		self.close()
		Gtk.main_quit()

if __name__ == "__main__":

	LP = LPInterdace()
	LP.show()

	Gtk.main()