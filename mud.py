import sched, time
import asyncio
import websockets
import json
import traceback
from run_command import Command
from player import Player
from attack import Attack
from log_utils import LogUtils, Level
from rooms import Rooms

class Mud:
    # number of players
    clients = []

    # create player
    name = "Crossen"
    hp = 10
    mana = 4
    location = 0
    perception = 30
    player = Player(name, hp, mana, location, perception)

    # prompt
    where_next_action = f"[HP={hp}/MA={mana}]: "

    async def exit_handler(self, signal, frame):
        LogUtils.info("An exit signal as been received.  Exiting!", logger)
        # exit stuff..

    async def notify_users(self):
        print('inside notify_users')
        json_msg = {
            "type": "get_clients",
            "value": len(self.clients)
        }

        print(f"Sending json to each connected client: {json.dumps(json_msg)}")
        for client in self.clients:
            print(f"Sending updated client list to {client['name']}")
            await client['socket'].send(json.dumps(json_msg))

    async def register(self, websocket):
        LogUtils.debug(f"A new client has connected, registering..", logger)
        # get the client hostname
        LogUtils.debug(f"Requesting client hostname..", logger)   
        await websocket.send('{"type": "request_hostname"}')
        LogUtils.debug(f"Awaiting client name response from client..", logger)
        msg = await websocket.recv()
        LogUtils.debug(f"Message received: {msg}", logger)
        websocket_client = json.loads(msg)
        ip = websocket.remote_address[0]
        LogUtils.debug(f"Request received from {ip}: {websocket_client['type']}", logger)
        if websocket_client['type'] == 'hostname_answer':
            LogUtils.debug(f"A guest ({ip}) on lab page has connected", logger)
            new_client = dict(name=websocket_client['host'], socket=websocket)
            self.clients.append(new_client)
            await self.notify_users()
        else:
            LogUtils.error(f"We shouldn't be here.. received request: {websocket_client['type']}", logger)

    async def unregister(self, websocket):
        LogUtils.debug(f"Unregistering client..", logger)
        self.clients = [i for i in self.clients if not (i['socket'] == websocket)] 
        await self.notify_users()

    async def main(self, websocket, path):
        # register client websockets
        await self.register(websocket)

        received_command = True
        try:
            response = ""
            while True:                
                # display room user is in
                for room in Rooms.rooms:
                    bottom_response = ""
                    if room["id"] == self.player.location:
                        LogUtils.debug(f"received_command: {received_command}", logger)
                        if received_command == True:
                            received_command = False
                            # get the   description
                            description = room["description"]

                            # show items
                            items = ""
                            if len(room['items']) > 0:
                                for item in room['items']:
                                    items += item.name + ', '
                                items = items[0:len(items)-2]

                            # offer possible exits
                            exits = ""
                            for available_exit in room["exits"]:
                                exits += available_exit['direction'] + ', '
                            exits = exits[0:len(exits)-2]

                            # show monsters
                            monsters = ""
                            for monster in room["monsters"]:
                                monsters += monster.name + ', '
                                # if there are monsters in the room, attack!
                                bottom_response += f"{monster.name} prepares to attack you!<br>"
                            monsters = monsters[0:len(monsters)-2]
 
                            json_msg = {
                                "type": 'room',
                                "name": room["name"],
                                "description": description,
                                "items": items,
                                "exits": exits,
                                "monsters": monsters,
                                "top_response": response,
                                "bottom_response": bottom_response
                            }

                            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                            await websocket.send(json.dumps(json_msg))

                        # wait for a command to be sent
                        LogUtils.info(f"Waiting for command...", logger)
                        message = await websocket.recv()
                        msg_obj = json.loads(message)

                        if msg_obj["type"] == "cmd":
                            LogUtils.debug(f"Received: cmd", logger)
                            received_command = True
                            self.player, response = Command.run_command(msg_obj["cmd"], room, self.player, logger)
                        else:
                            LogUtils.error(f"Received unknown message: {message}", logger)
        except KeyboardInterrupt:
            loop.stop()
        except:
            LogUtils.error(f"An error occurred!\nException:\n{traceback.format_exc()}", logger)
        finally:
            LogUtils.info("Unregistering client!", logger)
            await self.unregister(websocket)

if __name__ == "__main__":
    try:
        # logger = LogUtils.get_logger(filename='mud.log', file_level=Level.DEBUG, console_level=Level.DEBUG, log_location="d:\\src\\mud", logger_name='websockets')
        logger = LogUtils.get_logger(filename='mud.log', file_level=Level.DEBUG, console_level=Level.DEBUG, log_location="d:\\src\\mud")
        m = Mud()

        # start websocket
        host = '127.0.0.1'
        port = '1234'
        LogUtils.info(f"Server started at {host}:{port}.  Waiting for client connections...", logger)
        
        # start websocket server
        LogUtils.info(f"Starting websocket server", logger)
        start_server = websockets.serve(m.main, host, port)

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
        LogUtils.error(f"An error occurred!\nException:\n{traceback.format_exc()}", logger)  
