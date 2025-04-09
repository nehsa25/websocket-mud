import asyncio
import websockets
import traceback
import sys
import os
import inspect
from log_utils import LogUtils
from sysargs_utils import SysArgs
from utility import Utility
from world import World
from world_state import WorldState
from flask import Flask, jsonify
import threading

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

        try:
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

            await self.handle_connection(player, websocket)

        except websockets.ConnectionClosedOK:
            LogUtils.warn(f"ConnectionClosedOK (client disconnected).", self.logger)
        except Exception as e:
            LogUtils.error(f"An error occurred!\nException: {e}", self.logger)
            LogUtils.error(traceback.format_exc(), self.logger)
        finally:
            LogUtils.debug(f"{method_name}: finally block executed.", self.logger)

    async def handle_connection(self, player, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player}", self.logger)
        try:
            while True:
                # Receive data from the client
                message = await websocket.recv()
                LogUtils.debug(f"{method_name}: Received message: {message}", self.logger)

                # Process the message
                await self.process_message(player, websocket, message)

        except websockets.ConnectionClosedOK:
            LogUtils.warn(f"ConnectionClosedOK (client disconnected).", self.logger)
            await self.world_state.players.unregister(player, self.world_state)
        except Exception as e:
            LogUtils.error(f"An error occurred!\nException: {e}", self.logger)
            LogUtils.error(traceback.format_exc(), self.logger)
        finally:
            LogUtils.debug(f"{method_name}: exit", self.logger)

    async def process_message(self, player, websocket, message):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player.name}, message: {message}", self.logger)
        try:
            # Parse the message as JSON
            data = json.loads(message)
            LogUtils.debug(f"{method_name}: Parsed JSON data: {data}", self.logger)

            # Handle different message types
            if data["type"] == MudEvents.COMMAND:
                # Process command
                command = data["cmd"]
                LogUtils.info(f"{method_name}: Received command: {command}", self.logger)
                await self.world.handle_command(player, command)
            else:
                LogUtils.warn(f"{method_name}: Unknown message type: {data['type']}", self.logger)

        except json.JSONDecodeError:
            LogUtils.error(f"{method_name}: Invalid JSON received: {message}", self.logger)
        except Exception as e:
            LogUtils.error(f"An error occurred!\nException: {e}", self.logger)
            LogUtils.error(traceback.format_exc(), self.logger)
        finally:
            LogUtils.debug(f"{method_name}: exit", self.logger)

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