import sched, time
import asyncio
import websockets
import json
import traceback
import random
from utility import Utility
from random import randint
from command import Command
from player import Player
from log_utils import LogUtils, Level
from sysargs_utils import SysArgs
from world import World

class Mud:
    # create our WORLD object that'll contain things like breeze and rain events
    world = World()

    # number of players
    combat_wait_secs = 3.5
    tasks = []
    room = None
    first_loop = True # send the room on first load
    attack_time = True # true so we run once to begin loop

    async def exit_handler(self, signal, frame):
        LogUtils.info("An exit signal as been received.  Exiting!", logger)
        # exit stuff..

    # used to update webpage on user count
    async def notify_users(self):
        print('inside notify_users')
        json_msg = {
            "type": "get_clients",
            "value": len(self.world.players)
        }

        print(f"Sending json to each connected client: {json.dumps(json_msg)}")
        for player in self.world.players:
            print(f"Sending updated client list to {player.name}")
            await player.websocket.send(json.dumps(json_msg))

    # calls at the beginning of the connection
    async def register(self, websocket):
        hp = 50
        strength = 3 # 0 - 30
        agility = 3 # 0 - 30
        location = 0
        perception = 50
        player = Player(hp, strength, agility, location, perception)

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
            player.name = websocket_client['host']
            player.websocket = websocket
            self.world.players.append(player)
            await self.notify_users()

            # send msg to everyone
            for world_player in self.world.players:
                if world_player.name == player.name:
                    await Utility.send_msg(f"Welcome {player.name}!", 'event', websocket, logger)
                else:
                    await Utility.send_msg(f"{player.name} joined the game!", 'event', world_player.websocket, logger)
        else:
            LogUtils.error(f"We shouldn't be here.. received request: {websocket_client['type']}", logger)
        return player

    # called when a client disconnects
    async def unregister(self, websocket):
        LogUtils.debug(f"Unregistering client..", logger)
        self.world.players = [i for i in self.world.players if not (i.websocket == websocket)] 
        await self.notify_users()

    # It begins to rain..
    async def rain(self, websocket):
        while True:
            rand = randint(1000, 3600)
            await asyncio.sleep(rand)
            await Utility.send_msg("It begins to rain..", 'event', websocket, logger)

            # wait for it to stop
            rand = randint(100, 500)
            await asyncio.sleep(rand)
            await Utility.send_msg("The rain pitter-patters to a stop and the sun begins to shine through the clouds..", 'event', websocket, logger)

    # You hear thunder off in the distane..
    async def thunder(self, websocket):
        while True:
            rand = randint(1000, 3800)
            await asyncio.sleep(rand)
            await Utility.send_msg("You hear thunder off in the distance..", 'event', websocket, logger)

    # A gentle breeze blows by you..
    async def breeze(self, websocket):        
        while True:
            rand = randint(1000, 3800)
            await asyncio.sleep(rand)
            await Utility.send_msg("A gentle breeze blows by you..", 'event', websocket, logger)

    # An eerie silence settles on the room..
    async def eerie_silence(self, websocket):
        while True:
            rand = randint(1000, 4000)
            await asyncio.sleep(rand)
            await Utility.send_msg("An eerie silence settles on the room..", 'event', websocket, logger)

    # shows color-coded health bar
    async def show_health(self, player, websocket):
        color = 'red'
        if player.hitpoints / player.max_hitpoints >= .75:
            color = 'green'
        elif player.hitpoints / player.max_hitpoints >= .25:
            color = 'yellow'

        health = f"Health: <span style=\"color: {color};\">{player.hitpoints}</span>"
        await Utility.send_msg(health, 'health', websocket, logger)

    # cancels all tasks and states you died if you die
    async def you_died(self, player, websocket):
        # set combat to false
        player.in_combat = False

        # cancel all tasks
        for task in self.tasks:
            task.cancel()

        # state you died
        await Utility.send_msg("You die.... but awaken in the crypt.", 'event', websocket, logger)
        
        # drop all items
        for item in player.inventory:
              self.room["items"].append(item)
        player.inventory = []

        # set player location to crypt
        player.location = 5

        # set hits back to max / force health refresh
        player.hitpoints = player.max_hitpoints
        await self.show_health(player, websocket)

        # force room refresh
        player, self.room, self.world = await Command.process_room(player.location, player, self.world, websocket, logger)
        pass

    # runs the combat
    async def start_mob_combat(self, player, websocket):
        # if the player is dead, don't do anything..
        if player.hitpoints <= 0:
            return player

        # let user know monsters are attacking them but wait before first attack
        found_monsters = False
        for monster in self.room["monsters"]:
            if not monster.name.lower().startswith('(dead)'):
                found_monsters = True

        if found_monsters == True:
            # we only want to print these messages the first time the user sees the monsters
            if player.in_combat == False:
                for monster in self.room["monsters"]:
                    if monster.is_alive == True:
                        await Utility.send_msg(f"{monster.name} prepares to attack you!", 'info', websocket, logger)

                # player is now in combat
                player.in_combat = True

                # wait before launching first attack
                await asyncio.sleep(self.combat_wait_secs)     
            
            # keep_attacking is set to True so we go into the loop but then false unless we find a valid monster
            keep_attacking = True
            while player.in_combat == True and keep_attacking == True:
                keep_attacking = False
                # force a sleep between rounds
                if self.attack_time == True: 
                    # perform monster attacks
                    for monster in self.room["monsters"]: # 3 monsters
                        if monster.is_alive == True:
                            keep_attacking = True
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

                            # check if monster is dead
                            if monster.is_alive == False:
                                found_monsters = True

                            # send our attack messages
                            await Utility.send_msg(response, 'attack', websocket, logger)
                            self.attack_time = False

                            # update hp
                            player.hitpoints = player.hitpoints - damage

                            # no point in continuing if player is dead..
                            if player.hitpoints <= 0:
                                player, self.room, self.world = await self.you_died(player, websocket)
                                break

                            await self.show_health(player, websocket)
                else:
                    # while combat is running, wait x seconds between rounds                
                    await asyncio.sleep(self.combat_wait_secs)
                    self.attack_time = True
                    keep_attacking = True
            
            # set in_combat to false once combat is over
            player.in_combat = False

            await Utility.send_msg("Combat ended.", 'info', websocket, logger)

            return player

    # main loop when client connects
    async def main(self, websocket, path):
        # register client websockets - runs onces each time a new person starts
        player = await self.register(websocket)

        try:
            # schedule some events that'll do shit
            self.world.breeze_task = asyncio.create_task(self.breeze(websocket))
            self.world.rain_task = asyncio.create_task(self.rain(websocket))
            self.world.eerie_task = asyncio.create_task(self.eerie_silence(websocket))
            self.world.thunder_task = asyncio.create_task(self.thunder(websocket))

            attack_task = None

            response = ""
            while True:
                # if we changed rooms, cancel attack <-- THIS IS WRONG.  THIS SHOULD BE DONE IN PROCESS_DIRECTION.
                if attack_task != None:
                    attack_task.cancel()

                # start combat (if monsters in room)
                attack_task = asyncio.create_task(self.start_mob_combat(player, websocket))
                self.tasks.append(attack_task)

                # send the room the player is in
                if self.first_loop == True:
                    player, self.room, self.world = await Command.process_room(player.location, player, self.world, websocket, logger)
                    self.first_loop = False

                # send updated hp
                await self.show_health(player, websocket)

                # wait for a command to be sent
                LogUtils.info(f"Waiting for command...", logger)
                message = await websocket.recv()
                msg_obj = json.loads(message)

                if msg_obj["type"] == "cmd":
                    LogUtils.debug(f"Received: cmd", logger)
                    received_command = True
                    player, self.room, self.world = await Command.run_command(msg_obj["cmd"], self.room, player, self.world, websocket, logger)
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
