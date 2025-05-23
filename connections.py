import websockets
from core.enums.events import EventEnum
from queues.game_message import GameMessage
from utilities.log_telemetry import LogTelemetryUtility
import asyncio


class Connections:
    connections = []

    def __init__(self, to_connections_queue: asyncio.Queue, to_world_queue: asyncio.Queue): 
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Connections")
        self.from_world_queue = to_world_queue
        self.to_world_queue = to_connections_queue

    async def connection_loop(self, websocket):
        try:
            # convert to event using EventGameInterface and fill in origin
            message: GameMessage = GameMessage(
                type=EventEnum.CONNECTION_NEW.value, 
                payload=None, 
                origin="connection", 
                websocket=websocket) 
            
            # this message is sent to the world queue to register the new connection
            await self.to_world_queue.put(message)

            # we then sit here while the connection is active, waiting for messages from the client
            while True:
                client_message = await websocket.recv()
                message: GameMessage = GameMessage(
                type=EventEnum.CLIENT_MESSAGE.value, 
                payload=client_message, 
                origin="connection", 
                websocket=websocket) 
                await self.to_world_queue.put(message)

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
