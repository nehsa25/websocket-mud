import inspect
import websockets
import traceback
from log_utils import LogUtils
from settings.exception import ExceptionUtils
from utility import MudEvents
import asyncio
import json
from command import Commands

class ConnectionHandler:
    def __init__(self, logger, world, world_state):
        self.logger = logger
        self.world = world
        self.world_state = world_state
        self.command = Commands(self.logger)

    async def handle_connection(self, player, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player}", self.logger)
        try:
            while True:
                # Receive data from the client
                message = await websocket.recv()
                LogUtils.debug(f"{method_name}: Received message: {message}", self.logger)

                # Process the message
                await self.process_message(player, message)

        except websockets.ConnectionClosedOK:
            LogUtils.warn(f"ConnectionClosedOK (client disconnected).", self.logger)
            await self.world_state.players.unregister(player, self.world_state)
        except Exception as e:
            LogUtils.error(f"Error: {ExceptionUtils.print_exception(e)}", self.logger)
        finally:
            LogUtils.debug(f"{method_name}: exit", self.logger)

    async def process_message(self, player, message):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player.name}, message: {message}", self.logger)

        # Parse the message as JSON
        data = json.loads(message)
        LogUtils.debug(f"{method_name}: Parsed JSON data: {data}", self.logger)

        # Handle different message types
        if data["type"] == MudEvents.EventTypes.get_event_type_id(MudEvents.EventTypes.COMMAND):
            command = data["cmd"]
            LogUtils.info(f"{method_name}: Received command: {command}", self.logger)
            await self.command.run_command(player, command, self.world_state)
        else:
            LogUtils.warn(f"{method_name}: Unknown message type: {data['type']}", self.logger)

    async def websocket_handler(websocket, path):
        while True:
            message = await websocket.recv()
            await websocket.send(f"Received message: {message}")

    async def exit_handler(self, signal, frame):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(
            f"{method_name}: enter, signal: {signal}, frame: {frame}", self.logger
        )
        LogUtils.info(
            f"{method_name}: An exit signal as been received.  Exiting!", self.logger
        )
        # exit stuff..
        LogUtils.debug(f"{method_name}: exit", self.logger)
    
# start websocket server
@staticmethod
async def start_websocket_server(mud, host, port, logger):        
    LogUtils.info(f"Starting websocket server on port {port}", logger)

    if host == None:
        async with websockets.serve(mud.main, "localhost", int(port), max_size=9000000):
            await asyncio.Future()  # Run forever
    else:
        async with websockets.serve(mud.main, host, int(port), max_size=9000000):
            await asyncio.Future()