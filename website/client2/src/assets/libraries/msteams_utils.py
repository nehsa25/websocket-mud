import re
import subprocess

class MSTeamsUtils(object):
	@staticmethod
	def clean_powershell_output(output, logger):
		stdout = re.split("Good day.*\n(.*)", output, flags=re.M)
		if len(stdout) == 1:
			stdout = output
		else:
			stdout = stdout[2]
		
		return stdout.strip()

	# we can't use the run_powershell_command in subprocess utils because it causes a circular dependency...
	@staticmethod
	def run_powershell_command(command, logger=None):
		try:
			output = None
			timeout_in_secs = 86400
			command = f"powershell.exe -command \"{command}\""
			output = subprocess.run(command, timeout=int(timeout_in_secs), shell=True, universal_newlines=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')
			output.stdout = MSTeamsUtils.clean_powershell_output(output.stdout, logger)
			return output
		except Exception as e:
			return str(e)	

	@staticmethod
	def send_msg(msg, title=None, channel='QA Automation', source='Python (script_utils)', success=True):
		cmd = f". $profile; send_msg -msg '{msg}'"

		if title != None:
			cmd += f" -title '{title}'"

		if channel != None:
			cmd += f" -channel '{channel}'"

		if source != None:
			cmd += f" -source '{source}'"

		if success != None:
			if success == True:
				cmd += f" -success $True"
			else:
				cmd += f" -success $False"

		return MSTeamsUtils.run_powershell_command(cmd)
