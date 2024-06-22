from enum import Enum

from log_utils import LogUtils

class Money:
    coppers = 0

    def get_coppers(self):
        # subtract drakes, gold, and silver from coppers
        return int(self.coppers % 1000 % 100 % 10)
    
    def get_silver(self):
        return int(self.coppers / 10)
    
    def get_gold(self):
        return int(self.coppers / 100)
    
    def get_drakes(self):
        return int(self.coppers / 1000)
    

    

