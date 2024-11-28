import sys

class SysArgs:
    @staticmethod
    def read_sys_args(keyword, delete_from_sysargv=True):
        arg_cnt = len(sys.argv)
        val = None
        for x in range(arg_cnt):
            if keyword in sys.argv[x]:
                val = sys.argv[x].split('=')[1]
                if delete_from_sysargv == True:
                    del sys.argv[x]
                break

        # if we didn't find the parameter altogether then return None..
        if val == None:
            return val
        elif val.lower() == 'true':
            return True
        elif val.lower() == 'false':
            return False
        elif val.isdigit():
            return int(val)
        else:
            return val
