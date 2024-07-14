import inspect
from log_utils import LogUtils
from utility import Utility


class PlayerClass(Utility):
    """Base class for all player classes.

    Args:
        Utility (_type_): _description_
    """
    logger = None
    telepathic = False

        