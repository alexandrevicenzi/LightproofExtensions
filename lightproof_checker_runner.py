
import sys

def help():
	pass

def run(*args):
	from lightproof_checker import LightproofCheckerCmd
	from lightproof_checker import LightproofCheckerGui
	L = LightproofCheckerCmd()
	L.compile_rules()
	L.proofread('')

if __name__ == '__main__':

	for arg in sys.argv[1:]:

		if arg == '--help' or arg == '--h':
			help()
		elif arg == '--cmd':
			run(mode='cmd')
		elif arg == '--gui':
			run(mode='gui')
		else:
			print 'Invalid parameter: ' + arg