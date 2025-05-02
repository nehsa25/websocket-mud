import websockets
from core.events.client_message import ClientMessageEvent
from core.events.connection_new import NewConnectionEvent
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
            self.logger.info("A connection was made!")
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


    # called when a client disconnects
    async def unregister(self, player, world_state, change_name=False):
        self.logger.debug(f"unregister: enter, player: {player.name}")
        self.logger.debug(f"self.players count: {len(self.players)}")
        self.players = [i for i in self.players if not i.websocket == player.websocket]
        await self.update_website_users_online(world_state)

        # # let folks know someone left
        # if change_name:
        #     await world_state.alert_world(
        #         f"{player.name} is changing their name..", player=player
        #     )
        # else:
        #     await world_state.alert_world(
        #         f"{player.name} left the game.", player=player
        #     )

        self.logger.info(f"new player count: {len(self.players)}")
        self.logger.debug("register: exit")
        return world_state

    # start websocket server
    async def start_websocket_server(self, mud, host, port):
        if host is None:
            async with websockets.serve(mud.main, "localhost", int(port), max_size=9000000):
                await asyncio.Future()  # Run forever
        else:
            async with websockets.serve(mud.main, host, int(port), max_size=9000000):
                await asyncio.Future()
