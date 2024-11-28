import os
import re
import subprocess

# from script utils
from log_utils import LogUtils

class SubprocessUtils:
	@staticmethod
	def clean_powershell_output(output, logger):
		stdout = re.split("Good day.*\n(.*)", output, flags=re.M)
		if len(stdout) == 1:
			stdout = output
		else:
			stdout = stdout[2]
		
		return stdout.strip()

	@staticmethod
	def run_powershell_command(command, logger=None, use_shell=True, execution_directory=None, timeout_in_secs=None):
		try:
			output = None
			cwd = os.getcwd()

			if execution_directory != None:				
				LogUtils.debug("Changing directory from {} to {}".format(os.getcwd(), execution_directory), logger)
				os.chdir(execution_directory)

			if use_shell == True:
				LogUtils.debug("Executing Powershell command " + command, logger)
			else:
				LogUtils.debug("Executing Powershell command " + " ".join(command), logger)

			if timeout_in_secs == None:
				LogUtils.debug("No timeout was specified.  Setting to 8 hours...", logger)
				timeout_in_secs = 60 * 60 * 8

			command = f"powershell.exe -command \"{command}\""
			output = subprocess.run(command, timeout=int(timeout_in_secs), shell=use_shell, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
			output.stdout = SubprocessUtils.clean_powershell_output(output.stdout, logger)

			# change back to previous cwd directory
			os.chdir(cwd)
			
			return output
		except Exception as e:
			return str(e)		

	@staticmethod
	def run_command(command, logger=None, use_shell=True, execution_directory=None, timeout_in_secs=None):
		try:
			output = None
			cwd = os.getcwd()

			if execution_directory != None:				
				LogUtils.debug("Changing directory from {} to {}".format(os.getcwd(), execution_directory), logger)
				os.chdir(execution_directory)

			if use_shell == True:
				LogUtils.debug("Executing batch command " + command, logger)
			else:
				LogUtils.debug("Executing batch command " + " ".join(command), logger)

			if timeout_in_secs == None:
				LogUtils.debug("No timeout was specified.  Setting to 1 day...", logger)
				timeout_in_secs = 86400

			output = subprocess.run(command, timeout=int(timeout_in_secs), shell=use_shell, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
			output.stdout = output.stdout.strip()
			
			# LogUtils.debug("command output:\nreturncode: {}\nstdout:\n{}\nstderr:\n{}".format(output.returncode, output.stdout, output.stderr), logger)

			# change back to previous cwd directory
			os.chdir(cwd)
			
			return output
		except Exception as e:
			return str(e)		
