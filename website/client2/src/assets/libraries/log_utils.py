import logging
import logging.handlers
import os
import socket
from enum import Enum

# from script utils
from slack_utils import SlackUtils
from msteams_utils import MSTeamsUtils

class Level(Enum):
	DEBUG = 'debug'
	INFO = 'info'
	WARN = 'warning'
	WARNING = 'warning'
	ERROR = 'error'
	CRITICAL = 'critical'

class LogUtils:
	@staticmethod
	def get_logger(filename, file_level, console_level=None, log_location="C:\\Tests", logger_name=None, log_size_bytes=5000000, backup_count=3):
		# create our directory if it doesn't exist
		if os.path.exists(log_location) != True:
			os.makedirs(log_location)
		
		# setup our logger
		if logger_name == None:
			logger = logging.getLogger(__name__)
		else: 
			logger = logging.getLogger(logger_name)
			
		logger_format = logging.Formatter("%(asctime)s [%(threadName)s] [%(levelname)s]  %(message)s")

		# for console
		console_handler = logging.StreamHandler()	
		console_handler.setFormatter(logger_format)

		# for log file
		file_handler = logging.handlers.RotatingFileHandler(os.path.join(log_location, filename), maxBytes=log_size_bytes, backupCount=backup_count)
		file_handler.setFormatter(logger_format)

		# if no steamwriter_level is passed, default to same as file_level
		if console_level == None:
			console_level = file_level

		# set the file log level
		if file_level.value == 'critical':
			file_handler.setLevel(logging.CRITICAL)
		elif file_level.value == 'error':
			file_handler.setLevel(logging.ERROR)
		elif file_level.value == 'warn' or file_level.value == 'warning':
			file_handler.setLevel(logging.WARN)
		elif file_level.value == 'info':
			file_handler.setLevel(logging.INFO)
		elif file_level.value == 'debug':
			file_handler.setLevel(logging.DEBUG)

		# set the console log level
		if console_level.value == 'critical':
			console_handler.setLevel(logging.CRITICAL)
		elif console_level.value == 'error':
			console_handler.setLevel(logging.ERROR)
		elif console_level.value == 'warn' or console_level.value == 'warning':
			console_handler.setLevel(logging.WARN)
		elif console_level.value == 'info':
			console_handler.setLevel(logging.INFO)
		elif console_level.value == 'debug':
			console_handler.setLevel(logging.DEBUG)

		# add the handlers to the logger object
		logger.addHandler(console_handler)
		logger.addHandler(file_handler)

		# allow all messages into the log (they're filtered by the handlers)
		logger.setLevel(logging.DEBUG)
		logger.propagate = False
		LogUtils.debug("logger started", logger)
		return logger

	@staticmethod
	def log_msg(msg, logger=None, level=None, send_slack=False, channel='qa-automation'):
		# get hostname
		hostname = socket.gethostname()

		if logger == None:
			# if logger not set, just print every message to screen
			print(msg + ' (logger == None)')
		elif level == logging.CRITICAL:
			logger.critical(msg)
		elif level == logging.ERROR:
			logger.error(msg)
		elif level == logging.WARNING:
			logger.warning(msg)
		elif level == logging.INFO:
			logger.info(msg)
		elif level == logging.DEBUG:
			logger.debug(msg)

		if send_slack == True:
			SlackUtils.send_msg_to_slack(f"{hostname.upper()}: {msg}", channel)

	@staticmethod
	def critical(msg, logger=None, send_slack=False, channel='qa-automation'):
		LogUtils.log_msg(msg, logger, logging.CRITICAL, send_slack, channel)

	@staticmethod
	def error(msg, logger=None, send_slack=False, channel='qa-automation'):
		LogUtils.log_msg(msg, logger, logging.ERROR, send_slack, channel)

	@staticmethod
	def warn(msg, logger=None, send_slack=False, channel='qa-automation'):
		LogUtils.log_msg(msg, logger, logging.WARNING, send_slack, channel)

	@staticmethod
	def info(msg, logger=None, send_slack=False, channel='qa-automation'):
		LogUtils.log_msg(msg, logger, logging.INFO, send_slack, channel)

	@staticmethod
	def debug(msg, logger=None, send_slack=False, channel='qa-automation'):
		LogUtils.log_msg(msg, logger, logging.DEBUG, send_slack, channel)

	@staticmethod
	def close(logger):
		LogUtils.debug("Closing logger", logger)
		handlers = logger.handlers[:]
		for handler in handlers:
			handler.close()
			logger.removeHandler(handler)
