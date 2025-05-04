from core.enums.send_scope import SendScopeEnum
from core.events.help import HelpEvent
from .attack import Attack
from .drop import Drop
from .equip import Equip
from .experience import Experience
from .get import Get
from .hide import Hide
from .look import Look
from .loot import Loot
from .move import Move
from .rest import Rest
from .say import Say
from .search import Search
from .statistics import Statistics
from .system import System
from .who import Who
from .inventory import Inventory
from core.enums.commands import CommandEnum
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility


class Help:
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
    type = CommandEnum.HELP

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

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Help() class")
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

    async def execute(self, player):
        self.logger.debug("Executing Help command")

        self.logger.debug("enter")

        # alert the room
        await InfoEvent(
            "You recall a small instructional pamphlet handed to you by the guard. You pull it out and begin to read."
        ).send(player.websocket)
        await InfoEvent(
            f"{player.name} pulls out a small, off-color pamphlet with a giant question mark on the cover and begins to read."
        ).send(player.websocket, scope=SendScopeEnum.ROOM, exclude_player=True)

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
        await HelpEvent(commands).send(player.websocket)
        self.logger.debug("exit")
