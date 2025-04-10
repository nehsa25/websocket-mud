import inspect
from log_utils import LogUtils
from utility import Utility


class Alignment:
    alignment = None
    
    def __init__(self, alignment, logger):
        self.logger = logger
        LogUtils.debug(f"Initializing alignment() class", logger)
        self.alignment = alignment
        
    async def is_opposing_alignment(self, npc, mob):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        opposing = False
        
        # you're good but I'm bad
        if mob.alignment == Utility.Alignment.GOOD and self.alignment == Utility.Alignment.EVIL:
           opposing = True
           
        # you're bad but I'm good
        elif mob.alignment  == Utility.Alignment.EVIL and self.alignment == Utility.Alignment.GOOD:
            opposing = True
            
        # you're evil and I'm either good or neutral
        elif mob.alignment  == Utility.Alignment.EVIL and (
            self.alignment == Utility.Alignment.GOOD or self.alignment == Utility.Alignment.NEUTRAL):
            opposing = True
        # you're fight anyone
        elif mob.alignment  == Utility.Alignment.CHOATIC:
            opposing = True 
        LogUtils.debug(f"{method_name}: Is npc \"{npc}\" opposed to \"{mob.name}\": {opposing}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return opposing