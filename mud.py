import sched, time
import asyncio
import websockets
import json
import traceback
from random import randint
from run_command import Command
from player import Player
from log_utils import LogUtils, Level
from rooms import Rooms
from sysargs_utils import SysArgs

class Mud:
    # number of players
    clients = []
    combat_wait_secs = 3.5

    # create player
    name = "Crossen"
    hp = 25
    mana = 4
    location = 0
    perception = 30
    player = Player(name, hp, mana, location, perception)

    async def exit_handler(self, signal, frame):
        LogUtils.info("An exit signal as been received.  Exiting!", logger)
        # exit stuff..

    # used to update webpage on user count
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

    # calls at the beginning of the connection
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

    # called when a client disconnects
    async def unregister(self, websocket):
        LogUtils.debug(f"Unregistering client..", logger)
        self.clients = [i for i in self.clients if not (i['socket'] == websocket)] 
        await self.notify_users()

    # It begins to rain..
    async def rain(self, websocket):
        while True:
            json_msg = { "type": 'event', "event": "It begins to rain.." }
            rand = randint(1, 1600)
            await asyncio.sleep(rand)
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

            # wait for it to stop
            rand = randint(100, 500)
            await asyncio.sleep(rand)
            json_msg = { "type": 'event', "event": "The rain pitter-patters to a stop and the sun begins to shine through the clouds.." }
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

    # A gentle breeze blows by you..
    async def breeze(self, websocket):        
        while True:
            json_msg = {
                "type": 'event',
                "event": "A gentle breeze blows by you..",
            }
            rand = randint(1, 1400)
            await asyncio.sleep(rand)
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

    # An eerie silence settles on the room..
    async def eerie_silence(self, websocket):
        while True:
            json_msg = {
                "type": 'event',
                "event": "An eerie silence settles on the room..",
            }
            rand = randint(500, 2000)
            await asyncio.sleep(rand)
            LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
            await websocket.send(json.dumps(json_msg))

    # runs the combat
    async def start_mob_combat(self, room, websocket):
        run_combat = False
        if len(room["monsters"]) > 0:
            run_combat = True

        while run_combat == True:
            for monster in room["monsters"]:
                # response = f"{monster.name} prepares to attack you!<br>"            
                obj = monster.damage.split('d')
                dice = int(obj[0])
                damage_potential = int(obj[1])
                damage_multipler = randint(0, damage_potential)

                # roll dice
                damage = dice * damage_multipler
                if damage > 0:
                    response = f"{monster.name} has hit you for {str(damage)}!"
                else:
                    response = f"{monster.name} missed!"
                
                # update hp
                self.player.hitpoints = self.player.hitpoints - damage

                json_msg = { "type": 'attack', "attack": response }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))

                # no point in continuing if player is dead..
                if self.player.hitpoints <= 0:
                    run_combat = False
                    json_msg = { "type": 'event', "event": "You died." }
                    LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                    await websocket.send(json.dumps(json_msg))
                    break

            # wait combat_wait seconds
            if run_combat == True:
                # send updated hp
                json_msg = { "type": 'health', "health": f"[HP={self.player.hitpoints}]" }
                LogUtils.debug(f"Sending json: {json.dumps(json_msg)}", logger)
                await websocket.send(json.dumps(json_msg))
                await asyncio.sleep(self.combat_wait_secs)

    # main loop when client connects
    async def main(self, websocket, path):
        # register client websockets
        await self.register(websocket)

        try:
            attack_task = None

            # schedule some events that'll do shit
            breeze_task = asyncio.create_task(self.breeze(websocket))
            rain_task = asyncio.create_task(self.rain(websocket))
            eerie_task = asyncio.create_task(self.eerie_silence(websocket))

            response = ""
            while True:
                # if we received a command
                if attack_task != None:
                    attack_task.cancel()

                # display room user is in
                room = [room for room in Rooms.rooms if room["id"] == self.player.location][0]

                # start combat
                attack_task = asyncio.create_task(self.start_mob_combat(room, websocket))

                bottom_response = ""
                if room["id"] == self.player.location:
                     # get the description
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
                        exits += available_exit['direction'][1] + ', '
                    exits = exits[0:len(exits)-2]

                    # show monsters
                    monsters = ""
                    for monster in room["monsters"]:
                        monsters += monster.name + ', '
                    monsters = monsters[0:len(monsters)-2]

                    # formulate message to client
                    json_msg = {
                        "type": 'room',
                        "name": room["name"],
                        "description": description,
                        "items": items,
                        "exits": exits,
                        "monsters": monsters,
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
                        self.player = await Command.run_command(msg_obj["cmd"], room, self.player, websocket, logger)
                    else:
                        LogUtils.error(f"Received unknown message: {message}", logger)
        except KeyboardInterrupt:
            loop.stop()
        except:
            LogUtils.error(f"An error occurred!\nException:\n{traceback.format_exc()}", logger)
        finally:
            await self.unregister(websocket)

if __name__ == "__main__":
    try:
        # logger = LogUtils.get_logger(filename='mud.log', file_level=Level.DEBUG, console_level=Level.DEBUG, log_location="d:\\src\\mud", logger_name='websockets')
        logger = LogUtils.get_logger(filename='mud.log', file_level=Level.DEBUG, console_level=Level.DEBUG, log_location="d:\\src\\websocket-mud")
        m = Mud()

        # start websocket
        host = SysArgs.read_sys_args("--host=")
        if host == None:
            host = '127.0.0.1'

        port = SysArgs.read_sys_args("--port=")
        if port == None:
            port = '81'

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
