# -*- encoding: UTF-8 -*-
# 2013 Alexandre Vicenzi (vicenzi.alexandre at gmail com)

import os
import sys
import zipfile

def unpack_oxt(file_name, dir_output, root_folder=True):

	if not zipfile.is_zipfile(file_name):
		return False

	with zipfile.ZipFile(file_name, "r") as z:

		if not os.path.exists(dir_output):
			os.makedirs(dir_output)

		for f in z.filelist:

			if root_folder:
				output = os.path.join(dir_output, os.path.basename(f.filename))
				fz = z.read(f)

				with open(output, 'w') as nf:
					nf.write(fz)

			else:
				z.extract(f.filename, dir_output)

	return True

def create_init_file(path):

	filename = os.path.join(path, '__init__.py')
	with open(filename, 'w') as f:
		f.write('# -*- encoding: UTF-8 -*-')

if __name__ == '__main__':

	if len(sys.argv) > 1:
		unpack_oxt(sys.argv[1], 'temp')
	else:
		print('Specify an OXT file.')