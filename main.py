import json
import os
import os.path
import isolated
import config



class Main:
	def run(self):
		# build list of files present
		self.files_raw = {}
		self.fill_filelist_raw(config.path_raw(), config.path_raw())
		self.files_view = {}
		self.fill_filelist_view(config.path_view(), config.path_view())
		self.files_sources = Sources()
		self.files_sources.read()

		# syncronize
		for (filename_noext, raw_details) in self.files_raw.iteritems():
			self.process_raw_file(filename_noext, raw_details)

		# views that dont have apropriate raws
		for (filename, view_details) in self.files_view.iteritems():
			if not view_details.has_key('processed'):
				print 'view file ' + view_details['cutoff_filename'] + \
					' has no apropriate raw'
				dest = 'deleted/' + os.path.basename(
					view_details['cutoff_filename'])
				isolated.move_file(config.path_view(), view_details['cutoff_filename'], 
					dest)





	def process_raw_file(self, filename_noext, raw_details):
		if not self.files_view.has_key(filename_noext):
			if not self.files_sources.has_key(filename_noext):
				# view file missing and wasnt mapped yet, converting
				isolated.convert_raw2view(filename_noext, raw_details)
				self.on_new_view_generated(filename_noext, raw_details)
			else:
				# view file missing and was mapped - means has been deleted
				# manually, delete raw too
				dest = 'deleted/' + os.path.basename(
					raw_details['cutoff_filename'])
				isolated.move_file(config.path_raw(), raw_details['cutoff_filename'], 
					dest)
		else:
			view_details = self.files_view[filename_noext]

			# filenames dont match, means view has been moved
			if view_details['cutoff_filename_noext'] != \
					raw_details['cutoff_filename_noext']:
				(f, raw_ext) = os.path.splitext(raw_details['cutoff_filename'])
				raw_dest_cutoff_filename = view_details['cutoff_filename_noext'] + raw_ext

				isolated.move_file(config.path_raw(), raw_details['cutoff_filename'], 
					raw_dest_cutoff_filename)

				# mark raw is in new position now
				raw_details['cutoff_filename'] = raw_dest_cutoff_filename
				raw_details['cutoff_filename_noext'] = view_details['cutoff_filename_noext']
				view_details['processed'] = '*'

				# todo - potentially view is out-of-date here

			elif not self.files_sources.has_key(filename_noext):
				print 'view details not known, converting'
				isolated.convert_raw2view(filename_noext, raw_details)
				self.on_new_view_generated(filename_noext, raw_details)

				view_details = self.files_view[filename_noext]
				view_details['processed'] = '*'
			else:
				source_details = self.files_sources.get(filename_noext)

				if view_details['size'] == source_details['view_size'] and \
						view_details['mtime'] == source_details['view_mtime'] and \
						raw_details['size'] == source_details['raw_size'] and \
						raw_details['mtime'] == source_details['raw_mtime']:
					print 'file is ok ' + view_details['cutoff_filename']
					view_details['processed'] = '*'
				else:
					print 'view details dont match, converting'
					isolated.convert_raw2view(filename_noext, raw_details)
					self.on_new_view_generated(filename_noext, raw_details)

					view_details = self.files_view[filename_noext]
					view_details['processed'] = '*'



	def fill_filelist_raw(self, cutoff_path, path):
		for filename in os.listdir(path):
			(filename_noext, ext) = os.path.splitext(filename)
			full_filename = os.path.join(path, filename)

			if filename == 'deleted':
				pass
			elif not os.path.isfile(full_filename):
				self.fill_filelist_raw(cutoff_path, full_filename)
			else:
				self.files_raw[filename_noext] = isolated.file_details(
					full_filename, cutoff_path)




	def fill_filelist_view(self, cutoff_path, path):
		for filename in os.listdir(path):
			(filename_noext, ext) = os.path.splitext(filename)
			full_filename = os.path.join(path, filename)

			if filename == 'deleted' or ext == '.avi' or ext == '.mov':
				pass
			elif not os.path.isfile(full_filename):
				self.fill_filelist_view(cutoff_path, full_filename)
			else:
				self.files_view[filename_noext] = isolated.file_details(
					full_filename, cutoff_path)


	def on_new_view_generated(self, filename_noext, raw_details):
		full_view_filename = os.path.join(config.path_view(), 
			raw_details['cutoff_filename_noext'] + '.jpg')

		self.files_view[filename_noext] = isolated.file_details(
			full_view_filename, config.path_view())
		self.files_sources.update(filename_noext, raw_details, 
			self.files_view[filename_noext])



# map of raw->view state
# todo: partition files storage by key
class Sources:
	def read(self, ):
		self.source_by_filename = {}

		if os.path.isfile(config.full_filename_sources()):
			try:
				with open(config.full_filename_sources(), 'r') as f:
					self.source_by_filename = json.loads(f.read())
			except ValueError:
				print 'failed to read ' + config.full_filename_sources()



	def has_key(self, k):
		return self.source_by_filename.has_key(k)



	def get(self, k):
		return self.source_by_filename[k]



	def update(self, filename_noext, raw_details, view_details):
		self.source_by_filename[filename_noext] = {
			'raw_size': raw_details['size'],
			'raw_mtime': raw_details['mtime'],
			'view_size': view_details['size'],
			'view_mtime': view_details['mtime']
		}

		print 'storing source for ' + view_details['cutoff_filename']

		with open(config.full_filename_sources(), 'w') as f:
			json.dump(self.source_by_filename, f)


o = Main()
o.run()