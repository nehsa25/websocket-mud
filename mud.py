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
from world_state import WorldState
from flask import Flask, jsonify
import threading

app = Flask(__name__)
logger = None  # Initialize logger at the top
mud = None     # Initialize mud instance at the top

class Mud(Utility):

    logger = None
    world = None
    world_state = None
    admin = None
    command = None
    utility = None
    COMBAT_WAIT_SECS = 3.5
    CHECK_FOR_MONSTERS_SECS = 2
    DEATH_RESPAWN_ROOM = 5
    REST_WAIT_SECS = 7
    monsters = []
    total_monsters = 0

    def __init__(self, logger) -> None:
        method_name = inspect.currentframe().f_code.co_name
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Mud() class", logger)
        self.world = World(self.logger)

        # session state
        self.world_state = WorldState(self.logger)

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

    # main loop when client connects
    async def main(self, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # register client websockets - runs onces each time a new person starts
        self.world_state = await self.world_state.players.new_user(
            self.world_state, websocket
        )

        player = None
        try:
            # enter our player input loop
            while True:
                # get current user
                player = await self.world_state.players.get_player(websocket)

                for p in self.world_state.players.players:
                    # set inventory for refresh
                    await p.send_inventory()

                    # send updated hp
                    await p.send_status()

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

                    await self.world.commands.run_command(
                        msg_obj["cmd"], player, self.world_state, extra_data
                    )
                else:
                    LogUtils.error(f"Received unknown message: {message}", self.logger)
        except websockets.ConnectionClosedOK:
            LogUtils.warn(f"Someone left. We're going to move on.", logger)
        except KeyboardInterrupt:
            loop.stop()
        except:
            LogUtils.error(
                f"An error occurred!\nException:\n{traceback.format_exc()}", logger
            )
        finally:
            if player is not None:
                await self.world_state.players.unregister(
                    player, self.world_state, False
                )

        LogUtils.debug(f"{method_name}: Done Done.", self.logger)

async def websocket_handler(websocket, path):
    while True:
        message = await websocket.recv()
        await websocket.send(f"Received message: {message}")

async def start_websocket_server(host, port):
    # start websocket server
    LogUtils.info(f"Starting websocket server on port {port}", logger)
    # ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # ssl_context.load_cert_chain(
    #     "certificate.pem", "private.key"
    # )

    if host == None:
        # async with websockets.serve(mud.main, "localhost", port, max_size=9000000, ssl=ssl_context):
        #     await asyncio.Future()  # Run forever
        async with websockets.serve(mud.main, "localhost", int(port), max_size=9000000):
            await asyncio.Future()  # Run forever
    else:
        async with websockets.serve(mud.main, host, int(port), max_size=9000000):
            await asyncio.Future()

@app.route("/health")
def health_check():
    service_healthy = True
    # Add any specific health checks here if needed
    if service_healthy:
        return jsonify({"status": "healthy", "service": "ok"}), 200
    else:
        return jsonify({"status": "unhealthy", "service": "error" if not service_healthy else "ok"}), 503

def start_flask_app(host, port):
    LogUtils.info(f"Starting Flask app on port {port}", logger)
    app.run(host=host, port=port, debug=False, use_reloader=False)

if __name__ == "__main__":
    try:
        logger = LogUtils.get_logger(
            filename="mud.log",
            file_level=Level.ERROR,
            console_level=Level.ERROR,
            log_location="~/",
        )
        mud = Mud(logger)

        # start websocket
        host = SysArgs.read_sys_args("--host=")
        port = SysArgs.read_sys_args("--port=")

        if host == None:
            host = "0.0.0.0"

        if port == None:
            port = 22009

        # start listening loop for world events
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(mud.world_state.setup_world_events())

        LogUtils.info(f"Server started at {host}:{port}.  Waiting for client connections...", logger)

        # Run both the websocket server and the Flask app concurrently
        websocket_task = loop.create_task(start_websocket_server(host, port))

        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=start_flask_app, args=(host, 22010))
        flask_thread.daemon = True
        flask_thread.start()

        # Wait for the websocket task to complete (it should run forever)
        loop.run_until_complete(websocket_task)

        # If the websocket task completes (which shouldn't happen in normal operation),
        # we can add cleanup here if needed.
        LogUtils.info(f"Exiting...", logger)
        sys.exit()
    except KeyboardInterrupt:
        LogUtils.info(f"Keyboard interrupt received. Shutting down...", logger)
        if loop.is_running():
            tasks = asyncio.all_tasks(loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        if loop.is_running():
            loop.stop()
    except Exception:
        LogUtils.error(
            f"An error occurred during startup or runtime!\nException:\n{traceback.format_exc()}", logger
        )
    finally:
        if loop.is_running():
            loop.close()