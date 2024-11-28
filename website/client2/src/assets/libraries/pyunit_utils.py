import os
import sys
import traceback
import unittest
from shutil import rmtree

# from script utils
from log_utils import LogUtils

class PyUnitUtils(object):

    @staticmethod
    def xml_runner_config(debug_mode, unittest, xmlrunner, tmp_path, move_path, filename, logger=None):
        file_tmp_full_path = "{}\\{}".format(tmp_path, filename)
        file_done_full_path = "{}\\{}".format(move_path, filename)

        # check if tmp directory exists
        if not (os.path.isdir(tmp_path)):
            LogUtils.debug(tmp_path + " doesn't exist.  Creating!", logger)
            os.makedirs(tmp_path)

        # check if result directory exists
        if not (os.path.isdir(move_path)):
            LogUtils.debug(move_path + " doesn't exist.  Creating!", logger)
            os.makedirs(move_path)

        # run the tests
        with open(file_tmp_full_path, 'w+', encoding='utf-8') as output:
            try:
                unittest.main(
                    testRunner=xmlrunner.XMLTestRunner(output=output, verbosity=3),
                    failfast=False,
                    buffer=False,
                    catchbreak=False,
                    exit=False)
            except SystemExit:
                LogUtils.warn("Ignoring this SystemExit exception but some day need to figure out how to fix it.  Details: " + traceback.format_exc(), logger)
            except:
                LogUtils.error("Exception throw executing Python unit tests:\n\t\t\"{}\"".format(traceback.format_exc()), logger)

        if debug_mode == True:
            LogUtils.debug("Debug_mode set to True.  Removing results file.", logger)
            os.remove(file_tmp_full_path)
        else:
            LogUtils.info("XML results will be saved to " + file_done_full_path, logger)
            os.replace(file_tmp_full_path, file_done_full_path)

    @staticmethod
    def assert_equals(expected, actual, msg=None):
        if msg == None:
            msg = ""

        if actual != expected:
            raise AssertionError("{}: Expected:\"{}\" != Actual: \"{}\"".format(msg, expected, actual))

    @staticmethod
    def assert_not_equals(expected, actual, msg=None):
        if msg == None:
            msg = ""

        if expected == None:
            expected = ""
        else:
            expected = str(expected)

        if actual == None:
            actual = ""
        else:
            actual = str(actual)

        if actual == expected:
            raise AssertionError(msg or "Expected:\"{}\" != Actual: \"{}\"\n{}".format(expected, actual, msg))

    @staticmethod
    def findall(v, k, logger):
        if type(v) == dict:
            for k1 in v.keys():
                LogUtils.info('Comparing \"{}\"-> \"{}\" to \"{}\"'.format(k1, k[k1], v[k1]), logger)
                PyUnitUtils.assert_equals(k[k1], v[k1])

    @staticmethod
    def assert_dict_equals(expected, actual, logger):
        PyUnitUtils.findall(expected, actual, logger)

    @staticmethod
    def assert_contains(snippet, full, msg=None):
        if snippet not in full:
            raise AssertionError(msg or "Snippet:{} not in Full Text:{}".format(snippet, full))

    @staticmethod
    def assert_true(is_true, msg=None):
        if(is_true != True):
            if (msg == None):
                raise AssertionError("Expected true but got false.")
            else:
                raise AssertionError(msg)

    @staticmethod
    def assert_fail(msg):
        raise AssertionError(msg)
