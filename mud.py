import asyncio
import websockets
import traceback
import sys
import os
import inspect
import json
from log_utils import LogUtils
from sysargs_utils import SysArgs
from utility import Utility, MudEvents
from world import World
from world_state import WorldState
from flask import Flask, jsonify
import threading
from utilities.connection import ConnectionHandler, start_websocket_server  # Import ConnectionHandler and start_websocket_server

app = Flask(__name__)
logger = None 
mud = None

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
        super().__init__(logger)  # Call the superclass's __init__ method
        self.logger = logger
        LogUtils.debug(f"{method_name}: Initializing Mud() class", logger)
        self.world = World(self.logger)

        # session state
        self.world_state = WorldState(self.logger)
        self.connection_handler = ConnectionHandler(self.logger, self.world, self.world_state)  # Instantiate ConnectionHandler

    # main loop when client connects
    async def main(self, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)

        # initialize world
        LogUtils.debug(f"{method_name}: Checking if self.world_state is None", self.logger)
        if self.world_state is None:
            LogUtils.info(f"{method_name}: self.world_state is None, initializing...", self.logger)
            self.world_state = WorldState(self.logger)
            LogUtils.info(f"{method_name}: self.world_state initialized.", self.logger)
        else:
            LogUtils.debug(f"{method_name}: self.world_state is already initialized.", self.logger)

        LogUtils.debug(f"{method_name}: Awaiting self.world_state.players.new_user...", self.logger)
        await self.world_state.players.new_user(
            self.world_state, websocket
        )
        LogUtils.debug(f"{method_name}: self.world_state.players.new_user completed.", self.logger)

        LogUtils.debug(f"{method_name}: Awaiting self.world_state.players.get_player...", self.logger)
        player = await self.world_state.players.get_player(websocket)
        LogUtils.debug(f"{method_name}: self.world_state.players.get_player completed, player: {player}", self.logger)

        await self.connection_handler.handle_connection(player, websocket)  # Use the ConnectionHandler

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
    # Define loop outside the try block
    loop = None
    try:
        print("Attempting to get logger...")

        # Determine the environment
        development_mode = False
        if len(sys.argv) > 1 and sys.argv[1] == "--development":
            development_mode = True

        if development_mode:
            from dev_env.development import file_level, console_level
            print("Using development environment")
        else:
            from dev_env.production import file_level, console_level
            print("Using production environment")

        logger = LogUtils.get_logger(
            filename="mud.log",
            file_level=file_level,
            console_level=console_level,
            log_location=os.getcwd()
        )
        print(f"Logger obtained: {logger}")
        print("Attempting to instantiate Mud...")
        mud = Mud(logger)
        print(f"Mud instantiated: {mud}")

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
        websocket_task = loop.create_task(start_websocket_server(mud, host, port, logger))

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
        if loop and loop.is_running():
            tasks = asyncio.all_tasks(loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        if loop and loop.is_running():
            loop.stop()
    except Exception:
        LogUtils.error(
            f"An error occurred during startup or runtime!\nException:\n{traceback.format_exc()}", logger
        )
    finally:
        if loop and loop.is_running():
            loop.close()