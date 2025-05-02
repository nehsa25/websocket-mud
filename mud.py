import asyncio
import os
import sys
from connections import Connections
from models.init_database import InitializeDatabase
from settings.global_settings import GlobalSettings
from utilities.log_telemetry import LogTelemetryUtility
from utilities.exception import ExceptionUtility
from utilities.system import SystemUtility
from core.world import World
from flask import Flask, jsonify
import threading
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

app = Flask(__name__)
logger = None
mud = None


class Mud:
    COMBAT_WAIT_SECS = 3.5
    CHECK_FOR_MONSTERS_SECS = 2
    DEATH_RESPAWN_ROOM = 5
    REST_WAIT_SECS = 7

    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Mud() class")

        # create our queues and pass them into both World and Connections so the two classes can communicate

        # Create a queue for messages from the world to connections
        self.to_connections_queue = asyncio.Queue()
        # Create a queue for messages from connections to the world
        self.to_world_queue = asyncio.Queue()

        # websocket connections
        self.connections = Connections(
            self.to_connections_queue, self.to_world_queue
        ) 

        # session state
        self.world = World(
            self.to_world_queue, self.to_connections_queue
        )


    # main loop when client connects
    async def main(self, websocket):
        await self.connections.connection_loop(websocket)


@app.route("/health")
def health_check():
    service_healthy = True
    # Add any specific health checks here if needed
    if service_healthy:
        return jsonify({"status": "healthy", "service": "ok"}), 200
    else:
        return jsonify({"status": "unhealthy", "service": "error" if not service_healthy else "ok"}), 503


def start_flask_app(host, port):
    logger.info(f"Starting Flask app on port {port}")
    app.run(host=host, port=port, debug=False, use_reloader=False)


if __name__ == "__main__":
    # Define loop outside the try block
    loop = None
    tracer_provider = None
    try:
        logger = LogTelemetryUtility.get_logger()

        # start listening loop for world events
        loop = asyncio.new_event_loop()

        development_mode = False
        reset_game_data = False

        for arg in sys.argv:
            if arg == "--development":
                development_mode = True
            elif arg == "--reset":
                reset_game_data = True

        if reset_game_data and os.path.exists(GlobalSettings.DATABASE_PATH):
            os.remove(GlobalSettings.DATABASE_PATH)
            logger.info("Game data reset. Database removed.")

        # populate dbs
        if not os.path.exists(GlobalSettings.DATABASE_PATH):
            db = InitializeDatabase()
            loop.run_until_complete(db.populatedb())

        mud = Mud()
        print(f"Mud instantiated: {mud}")

        # start websocket
        host = SystemUtility.read_sys_args("--host=")
        port = SystemUtility.read_sys_args("--port=")

        if host is None:
            host = "0.0.0.0"

        if port is None:
            port = 22009

        asyncio.set_event_loop(loop)

        # Start the queue processing task
        loop.create_task(mud.world.process_connections_queue())

        # the world needs to run independently of the websocket server
        loop.run_until_complete(mud.world.setup_world())

        logger.info(f"Server started at {host}:{port}.  Waiting for client connections...")

        # Run both the websocket server and the Flask app concurrently
        websocket_task = loop.create_task(mud.connections.start_websocket_server(mud, host, port))

        # Wait for the websocket task to complete (it should run forever)
        loop.run_until_complete(websocket_task)

        # Start Flask app in a separate thread
        flask_thread = threading.Thread(target=start_flask_app, args=(host, 22010))
        flask_thread.daemon = True
        flask_thread.start()

        # If the websocket task completes (which shouldn't happen in normal operation),
        # we can add cleanup here if needed.
        logger.info("Exiting...")
        sys.exit()
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received. Shutting down...")
        if loop and loop.is_running():
            tasks = asyncio.all_tasks(loop)
            for task in tasks:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*tasks, return_exceptions=True))
        if loop and loop.is_running():
            loop.stop()
    except Exception as e:
        logger.error(f"Error: {ExceptionUtility.get_exception_information(e)}")
    finally:
        if loop and loop.is_running():
            loop.close()

        # Shutdown OpenTelemetry
        if tracer_provider:
            tracer_provider.shutdown()
