from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC

# from script utils
from log_utils import LogUtils

class SeleniumUtils(object):
    @staticmethod
    ##
    # <summary> Implicate wait. </summary>
    #
    # <param name="self">           The class instance that this method operates on. </param>
    # <param name="driver">         The driver. </param>
    # <param name="find_type">      Type of the find. </param>
    # <param name="search_string">  The search string. </param>
    # <param name="optional time">  The optional time. </param>
    def implicate_wait(driver, find_type, search_string, time_wait=None):
        wait_in_secs = 60 * 5

        try:
            return WebDriverWait(driver, wait_in_secs).until(EC.presence_of_element_located((find_type, search_string)))
        except TimeoutException as err:
            raise TimeoutException('Failed to find element "{}" (by {}) within {} second.  Error: {}'.format(
                search_string,
                find_type,
                str(time_wait),
                err
            ))	

    @staticmethod
    def wait_for_page_load(driver, page_url, logger=None):
        max_wait = 60 * 5

        for x in range(max_wait):
            if driver.current_url != page_url:
                sleep(1)
            else:
                LogUtils.debug("Sleeping 2 seconds to wait for page to fully render", logger)
                sleep(5)
                break
