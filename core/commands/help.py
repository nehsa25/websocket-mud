from core.data.player_data import PlayerData
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

    async def execute(self, player: PlayerData):
        self.logger.debug("Executing Help command")

        self.logger.debug("enter")

        # alert the room
        await InfoEvent(
            "You recall a small instructional pamphlet handed to you by the guard. You pull it out and begin to read."
        ).send(player.websocket)
        await InfoEvent(
            f"{player.selected_character.name} pulls out a small, off-color pamphlet with a giant question mark on the cover and begins to read."
        ).send(player.websocket, scope=SendScopeEnum.ROOM, exclude_player=True)

        commands = []
        commands.append(self.look.description)
        commands.append(self.get.description)
        commands.append(self.inventory.description)
        commands.append(self.drop.description)
        commands.append(self.search.description)
        commands.append(self.move.description)
        commands.append(self.experience.description)
        commands.append(self.hide.description)
        commands.append(self.statistics.description)
        commands.append(self.equip.description)
        commands.append(self.attack.description)
        commands.append(self.loot.description)
        commands.append(self.who.description)
        commands.append(self.rest.description)
        commands.append(self.say.description)
        commands.append(self.system.description)
        await HelpEvent(commands).send(player.websocket)
        self.logger.debug("exit")
