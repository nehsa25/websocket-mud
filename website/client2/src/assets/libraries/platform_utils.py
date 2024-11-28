import platform

from log_utils import LogUtils


class PlatformUtils:

    @staticmethod
    def is_windows_64bit(logger=None):
        bits, linkage =  platform.architecture()
        LogUtils.info("Bits: " + bits, logger, False)
        return bits == '64bit'
        