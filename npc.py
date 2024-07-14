import inspect
from log_utils import LogUtils
from npcs.alchemist import Alchemist
from npcs.armorer import Armorer
from npcs.blacksmith import Blacksmith
from npcs.gardener import Gardener
from npcs.guard import Guard
from npcs.healer import Healer
from npcs.innkeeper import InnKeeper
from npcs.maximus import Maximus
from npcs.merchant import Merchant
from npcs.princess import Princess
from npcs.sheriff import Sheriff
from npcs.thief import Thief
from npcs.wizard import Wizard
from utility import Utility


class Npc(Utility):
    logger = None
    
    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Npc() class", logger)
              
    def get_npc(self, npc_type, room_id):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)        
        npc = None
        if npc_type == Utility.Share.Npcs.SHERIFF:
            npc = Sheriff(self.logger)
        if npc_type == Utility.Share.Npcs.ALCHEMIST:
            npc = Alchemist(self.logger)
        if npc_type == Utility.Share.Npcs.BLACKSMITH:
            npc = Blacksmith(self.logger)
        if npc_type == Utility.Share.Npcs.GUARD:
            npc = Guard(self.logger)
        if npc_type == Utility.Share.Npcs.HEALER:
            npc = Healer(self.logger)
        if npc_type == Utility.Share.Npcs.INNKEEPER:
            npc = InnKeeper(self.logger)
        if npc_type == Utility.Share.Npcs.MERCHANT:
            npc = Merchant(self.logger)
        if npc_type == Utility.Share.Npcs.THIEF:
            npc = Thief(self.logger)
        if npc_type == Utility.Share.Npcs.WIZARD:
            npc = Wizard(self.logger)
        if npc_type == Utility.Share.Npcs.ARMORER:
            npc = Armorer(self.logger)
        if npc_type == Utility.Share.Npcs.PRINCESS:
            npc = Princess(self.logger)
        if npc_type == Utility.Share.Npcs.GARDENER:
            npc = Gardener(self.logger)
        if npc_type == Utility.Share.Npcs.MAXIMUS:
            npc = Maximus(self.logger)
            
        npc = npc.generate(room_id)
                     
        LogUtils.debug(f"{method_name}: exit", self.logger)
        return npc

                    
        

        