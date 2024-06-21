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

    async def alert_room(self, message, room, exclude_player=False, player = None, event_type=MudEvents.InfoEvent):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, message: {message}", self.logger)
        for p in room.players:
            if exclude_player and player is not None:
                if p.name != player.name:
                    LogUtils.info(f"{method_name}: alerting {p.name} of \"{message}\"", self.logger)
                    await self.send_message(event_type(message), p.websocket)
            else:
                await self.send_message(event_type(message), p.websocket)
    
    async def alert_world(self, message, world, exclude_player=True, player = None, event_type=MudEvents.InfoEvent):
        LogUtils.debug(f"alert_world: enter, message: {message}", self.logger)
        for p in world.players.players:
            if exclude_player and player is not None:
                if p.name != player.name:
                    await self.send_message(event_type(message), p.websocket)
            else:
                await self.send_message(MudEvents.InfoEvent(message), p.websocket)
                
        LogUtils.debug(f"alert_world: exit", self.logger)

    async def send_message(self, event_object, websocket):
        method_name = inspect.currentframe().f_code.co_name
        msg = event_object.to_json()        
        LogUtils.debug(f"{method_name}: enter, {msg}", self.logger)        
        LogUtils.debug(f"{method_name}: Sending json: {msg}", self.logger)
        LogUtils.debug(f"{method_name}: exit", self.logger)
        await websocket.send(str(msg))

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

    def sanitize_filename(self, filename):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        new_filename = "".join(i for i in filename if i.isalnum())
        LogUtils.debug(f"{method_name}: exit, returning: {new_filename}", self.logger)
        return new_filename