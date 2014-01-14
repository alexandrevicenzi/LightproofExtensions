# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os
import sys

def help():
	print('Usage: mode [options]')
	print('Mode parameters:')
	print('  cmd       execute using command line.')
	print('  gui       execute using a GUI Iinterface (default).')
	print('Options parameters:')
	print('  compile   just compile lang rules and check for errors.')
	print('  proofread just exec proofread and check for errors.')
	print('  oxt       OXT file to be used.')
	print('  input     Input file to test and assert proofread.')
	print('')

def run(**args):
	'''  '''
	mode = args.get('mode')
	opt = args.get('opt')

	if not mode:
		return

	if mode == 'cmd':
		from lightproof_checker import LightproofCheckerCmd
		L = LightproofCheckerCmd()
	elif mode == 'gui':
		from lightproof_checker import LightproofCheckerGui
		L = LightproofCheckerGui()
	else:
		print('Invalid mode: ' + mode)
		return

	if opt and 'compile' in opt:
		L.compile_rules()
	if opt and 'proofread' in opt:
		L.proofread('')

if __name__ == '__main__':

	mode = []
	opt = None
	oxt = None
	input = None

	for arg in sys.argv[1:]:

		if arg == '--help' or arg == '--h':
			help()
			sys.exit(0)
		elif arg == '-cmd':
			mode = 'cmd'
		elif arg == '-gui':
			mode = 'gui'
		elif arg == '-compile':
			mode.append('compile')
		elif arg == '-proofread':
			mode.append('proofread')
		elif arg.startswith('-oxt'):
			x = arg.find('=')
			
			if x > -1:
				oxt = arg[x + 1:]

				if not os.path.exists(oxt):
					print('File not found: ' + oxt)
					sys.exit(0)
				elif not os.path.isfile(oxt):
					print('Invalid file: ' + oxt)
					sys.exit(0)
			else:
				print 'File not present. Invalid parameter: -oxt'
				sys.exit(0)
		elif arg.startswith('-input'):
			x = arg.find('=')
			
			if x > -1:
				input = arg[x + 1:]

				if not os.path.exists(input):
					print('File not found: ' + input)
					sys.exit(0)
				elif not os.path.isfile(input):
					print('Invalid file: ' + input)
					sys.exit(0)
			else:
				print 'File not present. Invalid parameter: -input'
				sys.exit(0)
		else:
			print('Invalid parameter: ' + arg)
			sys.exit(0)

	if not mode:
		print('Choose mode.')
		help()
		sys.exit(0)
	# if not opt:
	# 	print('')
	# 	sys.exit(0)
	if opt and not oxt:
		print('Specify an OXT file.')
		sys.exit(0)
	if opt and 'proofread' in opt and not input:
		print('Specify an input file.')
		sys.exit(0)

	run(mode=mode, opt=opt, oxt=oxt, input=input)