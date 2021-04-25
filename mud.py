import sched, time
import asyncio
import websockets
import json
import traceback
from shared import Shared
from random import randint
from run_command import Command
from player import Player
from log_utils import LogUtils, Level
from sysargs_utils import SysArgs
from world import World

class Mud:
    # create our WORLD object that'll contain things like breeze and rain events
    world = World()

    # number of players
    clients = []
    combat_wait_secs = 3.5
    tasks = []
    room = None
    first_loop = True # send the room on first load
    attack_time = True # true so we run once to begin loop

    # create player
    name = "Crossen"
    hp = 50
    strength = 2 # 0 - 30
    agility = 2 # 0 - 30
    location = 0
    perception = 50
    player = Player(name, hp, strength, agility, location, perception)

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
            rand = randint(500, 1600)
            await asyncio.sleep(rand)
            await Shared.send_msg("It begins to rain..", 'event', websocket, logger)

            # wait for it to stop
            rand = randint(100, 500)
            await asyncio.sleep(rand)
            await Shared.send_msg("The rain pitter-patters to a stop and the sun begins to shine through the clouds..", 'event', websocket, logger)

    # A gentle breeze blows by you..
    async def breeze(self, websocket):        
        while True:
            rand = randint(500, 2800)
            await asyncio.sleep(rand)
            await Shared.send_msg("A gentle breeze blows by you..", 'event', websocket, logger)

    # An eerie silence settles on the room..
    async def eerie_silence(self, websocket):
        while True:
            rand = randint(500, 2000)
            await asyncio.sleep(rand)
            await Shared.send_msg("An eerie silence settles on the room..", 'event', websocket, logger)

    # shows color-coded health bar
    async def show_health(self, websocket):
        color = 'red'
        if self.player.hitpoints / self.player.max_hitpoints >= .75:
            color = 'green'
        elif self.player.hitpoints / self.player.max_hitpoints >= .25:
            color = 'yellow'

        health = f"Health: <span style=\"color: {color};\">{self.player.hitpoints}</span>"
        await Shared.send_msg(health, 'health', websocket, logger)

    # cancels all tasks and states you died if you die
    async def you_died(self, websocket):
        # set combat to false
        self.player.in_combat = False

        # cancel all tasks
        for task in self.tasks:
            task.cancel()

        # state you died
        await Shared.send_msg("You die.... but awaken in the crypt.", 'event', websocket, logger)
        
        # drop all items
        for item in self.player.inventory:
              self.room["items"].append(item)
        self.player.inventory = []

        # set player location to crypt
        self.player.location = 5

        # set hits back to max
        self.player.hitpoints = self.player.max_hitpoints

        # force room refresh
        self.room = [room for room in Rooms.rooms if room["id"] == self.player.location][0]

    # runs the combat
    async def start_mob_combat(self, websocket):
        # if the player is dead, don't do anything..
        if self.player.hitpoints <= 0:
            self.combat_started = False
            return player

        # let user know monsters are attacking them but wait before first attack
        if len(self.room["monsters"]) > 0:

            # we only want to print these messages the first time the user sees the monsters
            if self.player.in_combat == False:
                for monster in self.room["monsters"]:
                    await Shared.send_msg(f"{monster.name} prepares to attack you!", 'info', websocket, logger)

                # player is now in combat
                self.player.in_combat = True

                # wait before launching first attack
                await asyncio.sleep(self.combat_wait_secs)     

        while self.player.in_combat == True and len(self.room["monsters"]) > 0:
            if self.attack_time == True: 
                # perform monster attacks
                for monster in self.room["monsters"]:
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

                    # send our attack messages
                    await Shared.send_msg(response, 'attack', websocket, logger)
                    self.attack_time = False

                    # update hp
                    self.player.hitpoints = self.player.hitpoints - damage
                    await self.show_health(websocket)

                    # no point in continuing if player is dead..
                    if self.player.hitpoints <= 0:
                        await self.you_died(websocket)
                        break
            else:
                # while combat is running, wait x seconds between rounds                
                await asyncio.sleep(self.combat_wait_secs)
                self.attack_time = True

        # set in_combat to false once combat is over
        self.player.in_combat = False

    # main loop when client connects
    async def main(self, websocket, path):
        # register client websockets - runs onces each time a new person starts
        await self.register(websocket)

        try:
            # schedule some events that'll do shit
            self.world.breeze_task = asyncio.create_task(self.breeze(websocket))
            self.world.rain_task = asyncio.create_task(self.rain(websocket))
            self.world.eerie_task = asyncio.create_task(self.eerie_silence(websocket))

            attack_task = None

            response = ""
            while True:
                # if we changed rooms, cancel attack <-- THIS IS WRONG.  THIS SHOULD BE DONE IN PROCESS_DIRECTION.
                if attack_task != None:
                    attack_task.cancel()

                # start combat (if monsters in room)
                attack_task = asyncio.create_task(self.start_mob_combat(websocket))
                self.tasks.append(attack_task)

                # send the room the player is in
                if self.first_loop == True:
                    self.player, self.room = await Command.process_room(self.player.location, self.player, websocket, logger)
                    self.first_loop = False

                # send updated hp
                await self.show_health(websocket)

                # wait for a command to be sent
                LogUtils.info(f"Waiting for command...", logger)
                message = await websocket.recv()
                msg_obj = json.loads(message)

                if msg_obj["type"] == "cmd":
                    LogUtils.debug(f"Received: cmd", logger)
                    received_command = True
                    self.player, self.room = await Command.run_command(msg_obj["cmd"], self.room, self.player, websocket, logger)
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
            host = '0.0.0.0'

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
