# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os
import re

from bridge import LightproofBridge
from gi.repository import Gtk, GObject
from gladebuilder import GladeWindow, thread_safe, open_dialog
from standalone import LightproofStandalone
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

		w = self.w.get()

		R = Runner()

		if w['libreoffice']:
			if w['file']:
				with open(w['input_file'], 'w') as f:
					input = f.read()
			elif w['text']:
				input = w['input_text']
			elif w['url']:
				pass
			else:
				pass

			mode = 'manual' if w['manual'] else 'deploy'

			R.libreoffice(w['spell'], w['grammar'], input, mode, w['oxt_file'], w['locale'])
		elif w['standalone']:
			R.standalone(w['integrity'] or w['both_opt'], w['compile'] or w['both_opt'])

	def on_btn_oxt_file_clicked(self, *args):
		filename = open_dialog()
		self.w.show({'oxt_file': filename})

	def on_bt_file_clicked(self, *args):
		filename = open_dialog()
		self.w.show({'input_file': filename})

	def save_state(self):
		pass

	def load_state(self):

		self.w.show({'libreoffice' : True, 
					 'spell' : True, 
					 'unit_test' : True,
					 'file' : True, 
					 'manual' : True, 
					})

		pass

class Runner(GladeWindow):

	def __init__(self):
		GladeWindow.__init__(self, 'ui.glade', 'runner')

	def libreoffice(self, spell, grammar, text, pkg_mode, pkg_path, locale):
		self.show()

		t = Thread(target=self.__libreoffice, args=(spell, grammar, text, pkg_mode, pkg_path, locale,))
		t.daemon = True
		t.start()

	def __libreoffice(self, spell, grammar, text, pkg_mode, pkg_path, locale):

		try:
			import subprocess

			if not locale:
				self.update_status('Provide a locale.')
				return

			if pkg_mode == 'manual':
				self.update_status('Install your package...')
				subprocess.call(['unopkg', 'gui'])
			elif pkg_mode == 'deploy':

				if not os.path.exists(pkg_path):
					self.update_status('File not found: ' + pkg_path)
					return

				self.update_status('Deployng package...')
				subprocess.call(['unopkg', '-v', '-f', '-s', pkg_path])
			else:
				pass

			B = LightproofBridge(locale, error_func=self.update_status)

			if spell:
				self.update_status('Starting Spell Checker...')
				text = unicode(text, "utf-8")

				for word in re.findall(r"[\w']+", text, re.UNICODE):
					sug = B.spell(word)

					if sug:
						self.update_status('%s: Not in dictionary. Suggestion: %s' % (word, ', '.join(sug)))
					else:
						self.update_status('%s: In dictionary.' % (word))

			if grammar:
				self.update_status('Starting Gramar Checker...')
				B.proofread(text)
		except Exception, e:
			self.update_status(e.message)

	def standalone(self, package, integrity, compile):
		self.show()

		t = Thread(target=self.__standalone, args=(package, integrity, compile,))
		t.daemon = True
		t.start()

	def __standalone(self, package, integrity, compile):
		try:
			S = LightproofStandalone()
			if integrity:
				self.update_status('Not implemented yet.')
				#self.update_status('Checking OXT package...')
				#S.check_package()

			if compile:
				self.update_status('Compiling OXT package...')
				S.load_package()
				ret = S.compile_rules()
				if len(ret) > 0:
					for e in ret:
						msg = '%s at position %d.\nExpression: %s\nLine: %s'\
							% (e['msg'], e['pos'], e['exp'], e['line'])
						self.append_text(msg)
				else:
					self.append_text('Success.')
		except Exception, e:
			self.update_status('Error: ' + e.message)

	@thread_safe
	def update_status(self, text):
		self.w.results.get_buffer().insert(self.w.results.get_buffer().get_end_iter(), text + "\n")

	def on_bt_close_clicked(self, *args):
		self.close()

	def on_results_delete_event(self, *args):
		self.close()

if __name__ == "__main__":

	Win = LightProofGui()
	Win.show()

	Gtk.main()