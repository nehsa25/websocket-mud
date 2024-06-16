import inspect
import random
from log_utils import LogUtils
from mudevent import MudEvents


class Utility(MudEvents):
    logger = None
    rooms = None

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Utility() class", self.logger)

    async def alert_world(self, world, message):
        LogUtils.debug(f"alert_world: enter, message: {message}", self.logger)
        for player in world.players.players:
            await self.utility.send_msg(message, "announcement", player.websocket)
        LogUtils.debug(f"alert_world: exit", self.logger)

    async def send_message(self, msg, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, {msg}", self.logger)
        LogUtils.debug(f"{method_name}: Sending json: {msg}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        await websocket.send(str(msg))

    async def send_msg(self, msg, message_type, websocket, extra=""):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        json_msg = self.EventEvent(message_type, msg, extra).to_json()
        LogUtils.debug(f"{method_name}: Sending json: {json_msg}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        await websocket.send(json_msg)

    def generate_location(self, rooms):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        id = random.choice(rooms).id
        LogUtils.debug(f"{method_name}: enter", self.logger)
        return id

    def generate_name(self):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        names = []
        names.append("Ley")
        names.append("Sirius")
        names.append("Capella")
        names.append("Regulus")
        names.append("Stride")
        names.append("Betelgeuse")
        names.append("Holo")
        name_choice = random.randint(0, len(names) - 1)

        # title list
        titles = []
        titles.append("the Brave")
        titles.append("the Cowardly")
        titles.append("the Fool")
        titles.append("the greedy")
        titles.append("the Prideful")
        titles.append("the Wise")
        title_choice = random.randint(0, len(titles) - 1)

        # combine name and title
        name = f"{names[name_choice]} {titles[title_choice]}"
        LogUtils.debug(f"{method_name}: exit, returing: {name}", self.logger)

        return name
