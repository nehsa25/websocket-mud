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
from utilities.log_telemetry import LogTelemetryUtility


class CommandHandler:
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
    async def run_command(self, player, command, extra=""):
        self.logger.debug("enter")
        self.logger.debug(f'Command: "{command}"')

        command = command.strip()
        lowercase_cmd = command.lower()

        # send back the command we received as info - (this could just be printed client side and save the traffic cost)
        await CommandEvent(command).send(player.websocket)

        # if the player is dead, don't do anything..
        # if player.current_hp <= 0:
        #     return player

        # process each command
        if lowercase_cmd == "help":  # display help
            await self.help.execute(player)
        elif self.world_service.environments.dirs.is_valid_direction(
            command
        ):  # process direction
            await self.move.execute(command, player)
        # a look command - could be at the room, a person, a monster, an item
        elif (command == "" or lowercase_cmd == "l" or lowercase_cmd == "look" or lowercase_cmd.startswith("l ") or lowercase_cmd.startswith("look ")):
            await self.look.execute(command, player)
        elif lowercase_cmd.startswith("g ") or command.startswith("get "):  # get
            await self.get.execute(command, player)
        elif (lowercase_cmd == "i" or lowercase_cmd == "inv" or lowercase_cmd == "inventory"):  # inv
            await self.inventory.execute(player)
        elif lowercase_cmd == "sea" or lowercase_cmd == "search":  # search
            await self.search.execute(player)
        elif (lowercase_cmd.startswith("d ") or lowercase_cmd.startswith("dr ") or lowercase_cmd.startswith("drop ")):  # drop
            await self.drop.execute(command, player)
        elif lowercase_cmd.startswith("hide ") or lowercase_cmd.startswith(
            "stash "
        ):  # hide
            await self.hide.execute(command, player)
        elif (lowercase_cmd.startswith("eq ") or lowercase_cmd.startswith("equip ") or lowercase_cmd.startswith("wield ")):  # eq
            await self.equip.execute(command, player)
        elif lowercase_cmd.startswith("system ") or lowercase_cmd.startswith(
            "sys "
        ):  # a system command like changing username
            await self.system.execute(command, extra, player)
        elif (lowercase_cmd == "stat" or lowercase_cmd == "stats" or lowercase_cmd == "statistics"):  # stat
            await self.statistics.execute(player)
        elif (lowercase_cmd.startswith("a ") or lowercase_cmd.startswith("att ") or lowercase_cmd.startswith("attack ")):  # attack
            item = await self.attack.execute(command, player)
            print("commands.py, attack item: ", item)
        elif lowercase_cmd == ("exp") or lowercase_cmd == ("experience"):  # experience
            await self.experience.execute(player)
        elif lowercase_cmd.startswith("loot "):  # loot corpse
            await self.loot.execute(command, player)
        elif lowercase_cmd == ("who"):
            await self.who.execute(player)
        elif lowercase_cmd.startswith("yell "):
            await self.yell.execute(command, player)
        elif lowercase_cmd.startswith("whisper "):
            await self.whisper.execute(command, player)
        elif lowercase_cmd.startswith("say "):
            await self.say.execute(command, player)
        elif lowercase_cmd.startswith("telepath "):
            await self.telepath.execute(command, player)
        elif lowercase_cmd == "rest":
            await self.rest.execute(player)
        else:  # you're going to say it to the room..
            await ErrorEvent(f'"{command}" is not a valid command.').send(player.websocket)

        self.logger.debug("exit")
        return player
