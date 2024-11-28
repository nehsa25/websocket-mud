import sys
if 'nt' in sys.builtin_module_names:
    import winreg
from enum import Enum

# from script utils
from subprocess_utils import SubprocessUtils
from registry_utils import RegistryUtils
from log_utils import LogUtils

class Scope(Enum):
    USER = 0
    SYSTEM = 1

class EnvironmVarUtils:
    @staticmethod
    def set_environment_variable(name, value, scope=Scope.USER, logger=None):
        output = None
        if scope == Scope.SYSTEM:
            LogUtils.debug('Setting environment variable: {}={} at SYSTEM scope'.format(name, value))
            output = SubprocessUtils.run_command('setx /M {} {}'.format(name, value), logger)
        else:
            LogUtils.debug('Setting environment variable: {}={} at USER scope'.format(name, value))
            output = SubprocessUtils.run_command('setx {} {}'.format(name, value), logger)

        return output

    @staticmethod
    def delete_environment_varaible(name, scope=Scope.USER, logger=None):
        output = None
        if scope == Scope.SYSTEM:
            LogUtils.debug('Deleting environment variable: {} at SYSTEM scope'.format(name))            
            output = RegistryUtils.delete_reg_key(winreg.HKEY_LOCAL_MACHINE, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", name, logger)
        else:
            LogUtils.debug('Deleting environment variable: {} at USER scope'.format(name))
            output = RegistryUtils.delete_reg_key(winreg.HKEY_CURRENT_USER, "Environment", name, logger)

        # need to broadcast the change to explorer now
        output = EnvironmVarUtils.set_environment_variable('dummytest', '""', logger)
  
        return output
