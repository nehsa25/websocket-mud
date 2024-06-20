import ssl
import asyncio
import websockets
import json
import traceback
import sys
import inspect
from log_utils import LogUtils, Level
from mudevent import MudEvents
from sysargs_utils import SysArgs
from utility import Utility
from world import World

class Mud(Utility):
    logger = None
    world = None
    admin = None
    command = None
    utility = None
    COMBAT_WAIT_SECS = 3.5
    CHECK_FOR_MONSTERS_SECS = 2
    DEATH_RESPAWN_ROOM = 5
    REST_WAIT_SECS = 7

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Mud() class", logger)
        self.world = World(
            self.logger
        )  # create our WORLD object that'll contain things like breeze and rain events

    async def exit_handler(self, signal, frame):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        LogUtils.info("An exit signal as been received.  Exiting!", self.logger)
        # exit stuff..
        LogUtils.debug(f"{method_name}: exit", self.logger)

    # main loop when client connects
    async def main(self, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # register client websockets - runs onces each time a new person starts
        await self.world.players.new_user(self.world, websocket)

        player = None
        try:
            # setup world events
            await self.world.setup_world_events()

            # enter our player input loop
            while True:
                # get current user
                player = await self.world.players.get_player(websocket)
                
                for p in self.world.players.players:
                    # set inventory for refresh
                    await p.send_inventory()

                    # send updated hp
                    await p.send_health()
                    
                # wait for a command to be sent
                LogUtils.info(f"Waiting for command...", self.logger)
                message = await websocket.recv()
                msg_obj = json.loads(message)
                extra_data = None

                if msg_obj["type"] == MudEvents.EventUtility.get_event_type_id(
                    MudEvents.EventUtility.EventTypes.COMMAND
                ):
                    LogUtils.debug(f"Received: " + json.dumps(msg_obj), self.logger)
                    if msg_obj["extra"] != None:
                        extra_data = msg_obj["extra"]

                    await self.world.command.run_command(
                        msg_obj["cmd"], player, self.world, extra_data
                    )
                else:
                    LogUtils.error(f"Received unknown message: {message}", self.logger)
        except KeyboardInterrupt:
            loop.stop()
        except:
            LogUtils.error(
                f"An error occurred!\nException:\n{traceback.format_exc()}", logger
            )
        finally:
            if player is not None:
                await self.world.players.unregister(player, self.world, False)

        LogUtils.debug(f"{method_name}: Done Done.", self.logger)
        
if __name__ == "__main__":
    try:
        # logger = LogUtils.get_logger(filename='mud.log', file_level=Level.DEBUG, console_level=Level.DEBUG, log_location="d:\\src\\mud", logger_name='websockets')
        logger = LogUtils.get_logger(
            filename="mud.log",
            file_level=Level.DEBUG,
            console_level=Level.INFO,
            log_location="c:\\src\\websocket-mud",
        )
        m = Mud(logger)

        # start websocket
        host = SysArgs.read_sys_args("--host=")
        if host == None:
            host = "192.168.68.68"

        port = SysArgs.read_sys_args("--port=")
        if port == None:
            port = 60049

        LogUtils.info(
            f"Server started at {host}:{port}.  Waiting for client connections...",
            logger,
        )

        # start websocket server
        LogUtils.info(f"Starting websocket server", logger)
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            "c:/src/websocket-mud/certificate.pem", "c:/src/websocket-mud/private.key"
        )
        start_server = websockets.serve(
            m.main, host, port, max_size=9000000, ssl=ssl_context
        )

        # start listening loop
        loop = asyncio.get_event_loop()
        loop.run_until_complete(start_server)
        loop.run_forever()

        # if we got here the loop was cancelled, just quit
        LogUtils.info(f"Exiting...", logger)
        sys.exit()
    except KeyboardInterrupt:
        loop.stop()
    except:
        LogUtils.error(
            f"An error occurred!\nException:\n{traceback.format_exc()}", logger
        )
