import textwrap

# from script utils
from log_utils import LogUtils

class StringUtils:
    @staticmethod
    def stringify_object(obj, indent=0, max_length=50, logger=None):
        string = ''
        found_string = False
        if isinstance(obj, list):
            for item in obj:
                # if it's a string just process it
                if isinstance(item, str) or isinstance(item, int):
                    string += '\n' + str(item)
                    found_string = True
                # if it's a dict or list, pass it back through this function
                elif isinstance(item, list) or isinstance(item, dict):
                    string += '\n' + StringUtils.stringify_object(item)
        elif isinstance(obj, dict):
            for item in obj:
                # if it's a string just process it
                if isinstance(obj[item], str) or isinstance(obj[item], int):
                    string += '\n{:<20}{:<30}'.format(item + ':', textwrap.fill(str(obj[item]), width=max_length))
                    found_string = True
                # if it's a dict or list, pass it back through this function
                elif isinstance(obj[item], list) or isinstance(obj[item], dict):
                    string += '\n{}:\n{}'.format(item, StringUtils.stringify_object(obj[item]))
           
        # only indent once
        if found_string == False:
            string = string[1:len(string)]
        else:
            string = string.lstrip()
            string = textwrap.indent(string, '   ')

        return string

