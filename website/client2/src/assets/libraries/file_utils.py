import os
from glob import glob

# from script utils
from slack_utils import SlackUtils
from log_utils import LogUtils

class FileUtils:
	@staticmethod
	def find_files_by_extension(path, extension, logger=None):
		current_path = os.getcwd()
		os.chdir(path)
		files = glob("*." + extension)
		os.chdir(current_path)
		return files

	@staticmethod
	def find_files(path, logger=None):
		LogUtils.info("looking for files and directories at: {}".format(path), logger)
		file_results = []
		file_count = 0
		folder_results = []
		folder_count = 0

		for root, dirs, files in os.walk(path):
			# return each file
			for filename in files:
				file_count += 1
				file_path = os.path.join(root, filename)
				file_results.append(
					dict(
						full_path=file_path, 
						create_date=os.stat(file_path).st_ctime,
						folder_path=root,
						filename=filename,
						size=os.path.getsize(file_path)
					)
				)

			# return each folder
			for folder in dirs:
				folder_count += 1
				folder_results.append(os.path.join(root, folder))

		LogUtils.debug("Found {} files and {} folders".format(file_count, folder_count), logger)
		return folder_results, file_results

	@staticmethod
	def remove_file(file_path, logger=None):
		if os.path.isfile(file_path) and os.path.exists(file_path):
			LogUtils.info("Deleting " + file_path, logger)
			os.remove(file_path)

	@staticmethod
	def remove_files(file_path, pattern, logger=None):
		if os.path.exists(file_path):
			search_pattern = os.path.join(file_path, pattern)
			LogUtils.info("Deleting {} at {}".format(pattern, file_path), logger)
			
			for f in glob(search_pattern):
				LogUtils.info("Deleting: " + f, logger)
				os.remove(f)
