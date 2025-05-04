from core.commands.attack import Attack
from core.commands.drop import Drop
from core.commands.equip import Equip
from core.commands.experience import Experience
from core.commands.get import Get
from core.commands.help import Help
from core.commands.hide import Hide
from core.commands.inventory import Inventory
from core.commands.look import Look
from core.commands.loot import Loot
from core.commands.move import Move
from core.commands.rest import Rest
from core.commands.say import Say
from core.commands.search import Search
from core.commands.statistics import Statistics
from core.commands.system import System
from core.commands.telepath import Telepath
from core.commands.who import Who
from core.events.command import CommandEvent
from core.events.error import ErrorEvent
from utilities.events import EventUtility
from utilities.log_telemetry import LogTelemetryUtility


class Command:
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

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Commands() class")
        self.attack = Attack()
        self.drop = Drop()
        self.get = Get()
        self.inventory = Inventory()
        self.look = Look()
        self.loot = Loot()
        self.move = Move()
        self.search = Search()
        self.experience = Experience()
        self.hide = Hide()
        self.statistics = Statistics()
        self.equip = Equip()
        self.who = Who()
        self.rest = Rest()
        self.say = Say()
        self.system = System()
        self.help = Help()
        self.telepath = Telepath()

    # main function that runs all the rest
    async def run_command(self, player, command, world_state, extra=""):
        self.logger.debug("enter")
        self.logger.debug(f'Command: "{command}"')

        command = command.strip()
        lowercase_cmd = command.lower()

        # send back the command we received as info - (this could just be printed client side and save the traffic cost)
        await CommandEvent(command).send(player.websocket)

        # if the player is dead, don't do anything..
        if player.current_hp <= 0:
            return player

        # process each command
        if lowercase_cmd == "help":  # display help
            player = await self.help.execute(player)
        elif world_state.environments.dirs.is_valid_direction(
            command
        ):  # process direction
            player = await self.move.execute(command, player, world_state)
        # a look command - could be at the room, a person, a monster, an item
        elif (command == "" or lowercase_cmd == "l" or lowercase_cmd == "look" or lowercase_cmd.startswith("l ") or lowercase_cmd.startswith("look ")):
            player = await self.look.execute(command, player, world_state)
        elif lowercase_cmd.startswith("g ") or command.startswith("get "):  # get
            player, world_state = await self.get.execute(command, player, world_state)
        elif (lowercase_cmd == "i" or lowercase_cmd == "inv" or lowercase_cmd == "inventory"):  # inv
            player = await self.inventory.execute(player)
        elif lowercase_cmd == "sea" or lowercase_cmd == "search":  # search
            player = await self.search.execute(player, world_state)
        elif (lowercase_cmd.startswith("d ") or lowercase_cmd.startswith("dr ") or lowercase_cmd.startswith("drop ")):  # drop
            player = await self.drop.execute(command, player, world_state)
        elif lowercase_cmd.startswith("hide ") or lowercase_cmd.startswith(
            "stash "
        ):  # hide
            player = await self.hide.execute(command, player, world_state)
        elif (lowercase_cmd.startswith("eq ") or lowercase_cmd.startswith("equip ") or lowercase_cmd.startswith("wield ")):  # eq
            player = await self.equip.execute(command, player)
        elif lowercase_cmd.startswith("system ") or lowercase_cmd.startswith(
            "sys "
        ):  # a system command like changing username
            player = await self.system.execute(command, extra, player, world_state)
        elif (lowercase_cmd == "stat" or lowercase_cmd == "stats" or lowercase_cmd == "statistics"):  # stat
            player = await self.statistics.execute(player)
        elif (lowercase_cmd.startswith("a ") or lowercase_cmd.startswith("att ") or lowercase_cmd.startswith("attack ")):  # attack
            item = await self.attack.execute(command, player, world_state)
            print("commands.py, attack item: ", item)
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
            await ErrorEvent(f'"{command}" is not a valid command.').send(player.websocket)

        self.logger.debug("exit")
        return player
