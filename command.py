import inspect
import traceback

# my stuff
from commands.attack import Attack
from commands.drop import Drop
from commands.equip import Equip
from commands.experience import Experience
from commands.get import Get
from commands.help import Help
from commands.hide import Hide
from commands.look import Look
from commands.loot import Loot
from commands.move import Move
from commands.rest import Rest
from commands.say import Say
from commands.search import Search
from commands.telepath import Telepath
from commands.statistics import Statistics
from commands.system import System
from commands.who import Who
from commands.inventory import Inventory
from log_utils import LogUtils
from mudevent import MudEvents
from utility import Utility

class Commands(Utility):
    class Example:
        example = ""
        result = ""
        def __init__(self, example, result):
            self.example = example
            self.result = result
            
    logger = None
    command_utility = None
    
    # commands
    help = None
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
        LogUtils.debug("Initializing Commands() class", self.logger)
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
        self.help = Help(logger)
        self.telepath = Telepath(logger)
        
    # main function that runs all the rest
    async def run_command(self, player, command, world_state, extra = ""):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        LogUtils.debug(f'Command: "{command}"', self.logger)
        
        command = command.strip()
        lowercase_cmd = command.lower()

        # send back the command we received as info - (this could just be printed client side and save the traffic cost)
        await self.send_message(MudEvents.CommandEvent(command), player.websocket)

        # if the player is dead, don't do anything..
        if player.stats.current_hp <= 0:
            return player

        # process each command
        if lowercase_cmd == "help":  # display help
            player = await self.help.execute(player)
        elif world_state.environments.dirs.is_valid_direction(command):  # process direction
            player = await self.move.execute(command, player, world_state)
        # a look command - could be at the room, a person, a monster, an item
        elif command == "" or lowercase_cmd == "l" or lowercase_cmd == "look" or lowercase_cmd.startswith("l ") or lowercase_cmd.startswith("look "):
            player = await self.look.execute(command, player, world_state)
        elif lowercase_cmd.startswith("g ") or command.startswith("get "):  # get
            player, world_state = await self.get.execute(command, player, world_state)
        elif lowercase_cmd == "i" or lowercase_cmd == "inv" or lowercase_cmd == "inventory":  # inv
            player = await self.inventory.execute(player)
        elif lowercase_cmd == "sea" or lowercase_cmd == "search":  # search
            player = await self.search.execute(player, world_state)
        elif lowercase_cmd.startswith("d ") or lowercase_cmd.startswith("dr ") or lowercase_cmd.startswith("drop "):  # drop
            player = await self.drop.execute(command, player, world_state)
        elif lowercase_cmd.startswith("hide ") or lowercase_cmd.startswith("stash "):  # hide
            player = await self.hide.execute(command, player, world_state)
        elif lowercase_cmd.startswith("eq ") or lowercase_cmd.startswith("equip ") or lowercase_cmd.startswith("wield "):  # eq
            player = await self.equip.execute(command, player)
        elif lowercase_cmd.startswith("system ") or lowercase_cmd.startswith("sys "):  # a system command like changing username
            player = await self.system.execute(command, extra, player, world_state)
        elif lowercase_cmd == "stat" or lowercase_cmd == "stats" or lowercase_cmd == "statistics":  # stat
            player = await self.statistics.execute(player)
        elif (lowercase_cmd.startswith("a ")  or lowercase_cmd.startswith("att ") or lowercase_cmd.startswith("attack ")):  # attack
            item = await self.attack.execute(command, player, world_state)
            print("commands.py, attack item: ", item) # this is the item that was attacked?
        elif lowercase_cmd == ("exp") or lowercase_cmd == ("experience"):  # experience
            player = await self.experience.execute(player)
        elif lowercase_cmd.startswith("loot "):  # loot corpse
            player = await self.loot.execute(command, player, world_state)
        elif lowercase_cmd == ("who"):
            player = await self.who.execute(player, world_state)
        elif lowercase_cmd.startswith("yell "):
            player = await self.yell.execute(command, player, world_state)
        elif lowercase_cmd.startswith("whisper "):
            player = await self.whisper.execute(command, player, world_state)
        elif lowercase_cmd.startswith("say "):
            player = await self.say.execute(command, player, world_state)
        elif lowercase_cmd.startswith("telepath "):
            player = await self.telepath.execute(command, player, world_state)
        elif lowercase_cmd == "rest":
            player, world_state = await self.rest.execute(player, world_state)
        else:  # you're going to say it to the room..
            await self.send_message(MudEvents.ErrorEvent(f'"{command}" is not a valid command.'), player.websocket)

        LogUtils.debug(f"{method_name}: exit", self.logger)
        return player
