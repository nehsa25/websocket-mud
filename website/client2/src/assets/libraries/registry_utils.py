import sys
if 'nt' in sys.builtin_module_names:
    import winreg
from enum import Enum

# from script utils
from log_utils import LogUtils

class BaseRegistry(Enum):
    if "winreg" in sys.modules:
        HKEY_CLASSES_ROOT = winreg.HKEY_CLASSES_ROOT
        HKEY_CURRENT_CONFIG = winreg.HKEY_CURRENT_CONFIG
        HKEY_USERS = winreg.HKEY_USERS
        HKEY_CURRENT_USER = winreg.HKEY_CURRENT_USER
        HKEY_LOCAL_MACHINE = winreg.HKEY_LOCAL_MACHINE
    else:
        HKEY_CLASSES_ROOT = None
        HKEY_CURRENT_CONFIG = None
        HKEY_USERS = None
        HKEY_CURRENT_USER = None
        HKEY_LOCAL_MACHINE = None

class RegValueType(Enum):
    if "winreg" in sys.modules:
        REG_BINARY = winreg.REG_BINARY
        REG_DWORD = winreg.REG_DWORD
        REG_DWORD_LITTLE_ENDIAN = winreg.REG_DWORD_LITTLE_ENDIAN
        REG_DWORD_BIG_ENDIAN = winreg.REG_DWORD_BIG_ENDIAN
        REG_EXPAND_SZ = winreg.REG_EXPAND_SZ
        REG_LINK = winreg.REG_LINK
        REG_MULTI_SZ = winreg.REG_MULTI_SZ
        REG_NONE = winreg.REG_NONE
        REG_QWORD = winreg.REG_QWORD
        REG_QWORD_LITTLE_ENDIAN = winreg.REG_QWORD_LITTLE_ENDIAN
        REG_SZ = winreg.REG_SZ
    else:
        REG_BINARY = None
        REG_DWORD = None
        REG_DWORD_LITTLE_ENDIAN =None
        REG_DWORD_BIG_ENDIAN = None
        REG_EXPAND_SZ = None
        REG_LINK = None
        REG_MULTI_SZ = None
        REG_NONE = None
        REG_QWORD = None
        REG_QWORD_LITTLE_ENDIAN = None
        REG_SZ = None

class RegistryUtils:
    @staticmethod
    def set_reg_value(base_registry, registry_path, sub_key_or_value, value, reg_value_type, logger=None):
        LogUtils.debug("Setting registry sub key/value {} to {} ({}) at path {}".format(sub_key_or_value, value, reg_value_type.name, base_registry.name + "\\" + registry_path), logger)        
        registry_key = winreg.OpenKey(base_registry.value, registry_path, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, sub_key_or_value, 0, reg_value_type.value, value)
        winreg.CloseKey(registry_key)

    @staticmethod
    def get_reg_value(base_registry, registry_path, sub_key_or_value, logger=None):
        LogUtils.debug("Getting registry sub key/value {} at path {}".format(sub_key_or_value, base_registry.name + "\\" + registry_path), logger)        
        registry_key = winreg.OpenKey(base_registry.value, registry_path, 0, winreg.KEY_READ)
        value = winreg.QueryValueEx(registry_key, sub_key_or_value)
        winreg.CloseKey(registry_key)
        return value[0]

    @staticmethod
    def delete_reg_key(base_registry, registry_path, sub_key_or_value, logger=None):
        # attempt to open a key to see if it exists
        registry_key = winreg.OpenKey(base_registry.value, registry_path, 0, winreg.KEY_ALL_ACCESS)
        LogUtils.debug("Deleting sub key/value {} at {}".format(sub_key_or_value, base_registry.name + '\\' + registry_path), logger)     
        winreg.DeleteValue(registry_key, sub_key_or_value)
