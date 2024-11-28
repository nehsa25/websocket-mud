import socket
import re

# from script utils
from log_utils import LogUtils

class IPUtils:
    @staticmethod
    def check_ipv6(value, logger=None):
        LogUtils.debug("Checking if {} is an IPV6 address".format(str(value)), logger)

        try:
            socket.inet_pton(socket.AF_INET6, value)
            LogUtils.debug("...yes it is!", logger)
            return True
        except socket.error:
            LogUtils.debug("...no it isn't!", logger)
            return False

    @staticmethod
    def check_ipv4(value, logger=None):
        LogUtils.debug("Checking if {} is an IPV6 address".format(str(value)), logger)
        try:
            socket.inet_aton(value)
            LogUtils.debug("...yes it is!", logger)
            return True
        except socket.error:
            LogUtils.debug("...no it isn't!", logger)
            return False

    @staticmethod
    def check_mac_address(value, logger=None):
        LogUtils.debug("Checking if {} is a mac address".format(str(value)), logger)
        if re.match("[0-9a-f]{2}([-:]?)[0-9a-f]{2}(\\1[0-9a-f]{2}){4}$", value.lower()):
            LogUtils.debug("...yes it is!", logger)
            return True
        else:
            LogUtils.debug("...no it isn't!", logger)
            return False