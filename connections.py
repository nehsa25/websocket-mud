import websockets
from core.enums.send_scope import SendScopeEnum
from core.events.client_message import ClientMessageEvent
from core.events.connection_new import NewConnectionEvent
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
import asyncio
from utilities.command import Command


class Connections:
    connections = []

    def __init__(self, to_connections_queue: asyncio.Queue, to_world_queue: asyncio.Queue): 
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.command = Command()
        self.from_world_queue = to_world_queue
        self.to_world_queue = to_connections_queue

    async def connection_loop(self, websocket):
        try:
            await InfoEvent("A connection was made!").send(
                websocket=websocket,
                scope=SendScopeEnum.WORLD, 
                exclude_player=True)
            msg = NewConnectionEvent(websocket)
            await self.to_world_queue.put(msg)

            while True:
                client_message = await websocket.recv()
                await self.to_world_queue.put(ClientMessageEvent(client_message, websocket))

        except Exception as e:
            self.logger.error(f"Error in connection loop: {e}")
        finally:
            self.logger.info("Connection ended.")

    async def exit_handler(self, signal, frame):
        self.logger.debug(f"enter, signal: {signal}, frame: {frame}")
        self.logger.info("An exit signal as been received.  Exiting!")
        # exit stuff..
        self.logger.debug("exit")

    # start websocket server
    async def start_websocket_server(self, mud, host, port):
        if host is None:
            async with websockets.serve(mud.main, "localhost", int(port), max_size=9000000):
                await asyncio.Future()  # Run forever
        else:
            async with websockets.serve(mud.main, host, int(port), max_size=9000000):
                await asyncio.Future()
