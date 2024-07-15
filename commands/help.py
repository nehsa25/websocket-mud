from doctest import Example
import inspect
from commands.attack import Attack
from commands.drop import Drop
from commands.equip import Equip
from commands.experience import Experience
from commands.get import Get
from commands.hide import Hide
from commands.look import Look
from commands.loot import Loot
from commands.move import Move
from commands.rest import Rest
from commands.say import Say
from commands.search import Search
from commands.statistics import Statistics
from commands.system import System
from commands.who import Who
from commands.inventory import Inventory
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Help(Utility):
    class CommandHelp:
        command = ""
        description = ""
        examples = []
        def __init__(self, command):
            self.command = command.command
            self.description = command.description
            self.examples = command.examples  
            
    logger = None
    command = "help"
    examples = []
    description = "Display help information."
    type = Utility.Share.Commands.HELP

    # commands
    attack = None
    drop = None
    get = None
    inventory = None
    look = None
    loot = None
    move = None
    search = None
    experience = None
    hide = None
    statistics = None
    equip = None
    who = None
    rest = None
    say = None
    system = None
    
    def __init__(self, logger):
        self.logger = logger
        LogUtils.debug("Initializing Help() class", self.logger)
        self.attack = Attack(logger)
        self.drop = Drop(logger)
        self.get = Get(logger)
        self.inventory = Inventory(logger)
        self.look = Look(logger)
        self.loot = Loot(logger)
        self.move = Move(logger)
        self.search = Search(logger)
        self.experience = Experience(logger)
        self.hide = Hide(logger)
        self.statistics = Statistics(logger)
        self.equip = Equip(logger)
        self.who = Who(logger)
        self.rest = Rest(logger)
        self.say = Say(logger)
        self.system = System(logger)

    async def execute(self, player):
        LogUtils.debug("Executing Help command", self.logger)
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        commands = []
        commands.append(self.CommandHelp(self.look))
        commands.append(self.CommandHelp(self.get))
        commands.append(self.CommandHelp(self.inventory))
        commands.append(self.CommandHelp(self.drop))
        commands.append(self.CommandHelp(self.search))
        commands.append(self.CommandHelp(self.move))
        commands.append(self.CommandHelp(self.experience))
        commands.append(self.CommandHelp(self.hide))
        commands.append(self.CommandHelp(self.statistics))
        commands.append(self.CommandHelp(self.equip))
        commands.append(self.CommandHelp(self.attack))
        commands.append(self.CommandHelp(self.loot))
        commands.append(self.CommandHelp(self.who))
        commands.append(self.CommandHelp(self.rest))
        commands.append(self.CommandHelp(self.say))
        commands.append(self.CommandHelp(self.system))        
        await self.send_message(MudEvents.HelpEvent(commands), player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)