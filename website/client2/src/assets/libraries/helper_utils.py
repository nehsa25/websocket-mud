import time

# from script utils
from log_utils import LogUtils

class HelperUtils:
    @staticmethod
    def sleep_for(wait_in_seconds, logger=None):
        LogUtils.info('Sleeping for {} seconds'.format(wait_in_seconds), logger)

        for i in range(wait_in_seconds, 0, -1):
            time.sleep(1)
            LogUtils.debug('...' + str(i), logger)

    @staticmethod
    def get_duration(start_time):
        duration = (time.time() - start_time) / 60
        if duration > 60:
            duration = '{:.1f}'.format(duration / 60)
        else:
            duration = '{:.1f}'.format(duration)

        return duration
