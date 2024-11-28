from urllib.parse import urlencode
from urllib.request import Request, urlopen
import requests

class SlackUtils(object):
	@staticmethod
	def send_msg_to_slack(msg, channel='qa-automation'):
		PAYLOAD = {'text': msg}
		CHANNEL1 = 'https://hooks.slack.com/services/<>'

		# default to qa-automation
		if channel == None or channel == 'qa-automation':
			return requests.post(QA_AUTOMATION_CHANNEL, json=PAYLOAD)
		# if we got here then something is wrong!	
		raise ValueError(f"Unknown channel: {channel}")
