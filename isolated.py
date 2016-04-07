import json
import os
import os.path
import config



def move_file(path_base, cutoff_filename_src, cutoff_filename_dest):
	print 'moving raw ' + cutoff_filename_src + \
		' to ' + cutoff_filename_dest

	dest_dirname = os.path.dirname(os.path.join(path_base, 
		cutoff_filename_dest))
	if len(dest_dirname) > 0 and not os.path.exists(dest_dirname):
		print 'creating dir ' + dest_dirname
		os.makedirs(dest_dirname)

	os.rename(os.path.join(path_base, cutoff_filename_src), 
		os.path.join(path_base, cutoff_filename_dest))



def convert_raw2view(filename_noext, raw_details):
	full_raw_filename = os.path.join(config.path_raw(), raw_details['cutoff_filename'])

	full_view_filename = os.path.join(config.path_view(), 
		raw_details['cutoff_filename_noext'] + '.jpg')

	full_view_dirname = os.path.dirname(full_view_filename)
	if len(full_view_dirname) > 0 and not os.path.exists(full_view_dirname):
		os.makedirs(full_view_dirname)

	commandline = config.convert_commandline()\
		.replace('{src}', full_raw_filename)\
		.replace('{dest}', full_view_filename)

	print commandline
	return_value = os.system(commandline)

	if return_value != 0:
		print 'failed to convert ' + full_raw_filename

	return return_value != 0



def file_details(full_filename, cutoff_path):
	stat = os.stat(full_filename)
	cutoff_filename = full_filename[len(cutoff_path):]

	(cutoff_filename_noext, ext) = os.path.splitext(cutoff_filename)

	return {
		'cutoff_filename': cutoff_filename,
		'cutoff_filename_noext': cutoff_filename_noext,
		'size': stat.st_size, 
		'mtime': stat.st_mtime
	}
