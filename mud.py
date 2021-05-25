from monster import Monster
import sched, time
import asyncio
import websockets
import json
import traceback
import random
import sys
from random import randint
from utility import Utility
from command import Command
from player import Player
from log_utils import LogUtils, Level
from sysargs_utils import SysArgs
from world import World
from monsters import Monsters
from rooms import Rooms

class Mud:
    world = World() # create our WORLD object that'll contain things like breeze and rain events
    COMBAT_WAIT_SECS = 3.5
    CHECK_FOR_MONSTERS_SECS = 2

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
        hp = 10
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

            # show room
            player, self.world = await self.world.move_room(player.location, player, self.world, websocket, logger)
        else:
            LogUtils.error(f"We shouldn't be here.. received request: {websocket_client['type']}", logger)
        return player

    # called when a client disconnects
    async def unregister(self, websocket):
        LogUtils.debug(f"Unregistering client..", logger)
        current_player = [i for i in self.world.players if i.websocket == websocket][0]
        self.world.players = [i for i in self.world.players if not (i.websocket == websocket)] 
        await self.notify_users()

        # let folks know someone left
        for world_player in self.world.players:
            await Utility.send_msg(f"{current_player.name} left the game.", 'event', world_player.websocket, logger)

    # shows color-coded health bar
    async def show_health(self, player, websocket):
        await Utility.send_msg(f"{str(player.hitpoints)}/{str(player.max_hitpoints)}", 'health', websocket, logger)

    # cancels all tasks and states you died if you die
    async def you_died(self, player, websocket):
        # set combat to false
        player.in_combat = False

        # state you died
        await Utility.send_msg("You die... but awaken on a strange beach shore.", 'event', websocket, logger)
        
        # drop all items
        room = await self.world.get_room(player.location)
        for item in player.inventory:
              room["items"].append(item)
        player.inventory = []

        # set player location to beach shore
        player, self.world = await self.world.move_room(5, player, self.world, websocket, logger)

        # set hits back to max / force health refresh
        player.hitpoints = player.max_hitpoints
        await self.show_health(player, websocket)

    # runs the combat
    async def start_mob_combat(self):
        # we never leave this attack loop
        while True:
            for player in self.world.players:
                LogUtils.debug(f"{player.name}: start_mob_combat - Running loop", logger)
                player_to_attack = None

                # Allow other tasks to complete
                await asyncio.sleep(.1)

                # get our room
                room = await self.world.get_room(player.location, logger)

                found_monsters = False

                # if there's no one in the room, pause to ensure we don't loop endlessly
                alive_monsters = [monster for monster in room['monsters'] if monster.is_alive == True]
                if len(alive_monsters) == 0:
                    await asyncio.sleep(self.CHECK_FOR_MONSTERS_SECS)

                # show the initial "prepares to attack you text"
                for monster in room["monsters"]:
                    if monster.is_alive == True:
                        found_monsters = True
                        LogUtils.debug(f"{player.name}: start_mob_combat - found monster", logger)

                        if monster.in_combat == None:
                            LogUtils.debug(f"{player.name}: start_mob_combat - monster is not on combat", logger)

                            # determine who to attack
                            player_to_attack = random.choice(room["players"])
                            
                            # set who monster is in combat with
                            monster.in_combat = player_to_attack.name
                            LogUtils.debug(f"{player.name}: start_mob_combat - monster now attacking {monster.in_combat}", logger)

                            # cycle through all players
                            for attack_player in room["players"]:
                                if monster.in_combat == attack_player.name:
                                    await Utility.send_msg(f"{monster.name} prepares to attack you!", 'info', attack_player.websocket, logger)
                                else:
                                    await Utility.send_msg(f"{monster.name} prepares to attack {attack_player.name}!", 'info', attack_player.websocket, logger)

                if found_monsters == True:
                    # wait before launching first attack
                    await asyncio.sleep(self.COMBAT_WAIT_SECS)
                    attack_time = True

                    # get our room
                    room = await self.world.get_room(player.location, logger)

                    # process attacks
                    total_damage = 0
                    monsters_damage = []
                    for monster in room["monsters"]:
                        if monster.is_alive == True:
                            # while combat is running, wait x seconds between rounds    
                            if attack_time != True:                                        
                                await asyncio.sleep(self.COMBAT_WAIT_SECS)

                            # need to check here if combat is still going.. we may have killed everything or moved rooms
                            if monster.is_alive == True:
                                # calculate our damage
                                obj = monster.damage.split('d')
                                dice = int(obj[0])
                                damage_potential = int(obj[1])
                                damage_multipler = randint(0, damage_potential)

                                # roll dice for a monster
                                damage = dice * damage_multipler
                                total_damage += damage

                                # add to our monster damage list
                                monster_damage = dict(name=monster.name, damage=damage)
                                monsters_damage.append(monster_damage)

                    # sort based on damage
                    monsters_damage = sorted(monsters_damage, key=lambda k: k['damage'], reverse=True) 

                    # build our attack message
                    attack_msg = f"You were hit for {total_damage} damage!"
                    attack_msg += " ("
                    for monster_damage in monsters_damage:
                        if monster_damage['damage'] > 0:
                            attack_msg += f"{monster_damage['name']}: {monster_damage['damage']}, "
                    attack_msg = attack_msg[0:len(attack_msg)-2]
                    attack_msg += ")"

                    # if there are still monsters alive
                    monsters_alive = False
                    for monster in room["monsters"]:
                        if monster.is_alive == True:
                            monsters_alive = True
                    if monsters_alive == True and monster.in_combat == player.name:
                        # send our attack messages                
                        if total_damage > 0:
                            await Utility.send_msg(attack_msg, 'attack', player.websocket, logger)
                        else:
                            await Utility.send_msg("No monsters dealt you any damage!", 'info', player.websocket, logger)

                        # update hp
                        player.hitpoints = player.hitpoints - total_damage

                        # no point in continuing if player is dead..
                        if player.hitpoints <= 0:
                            await self.you_died(player, player.websocket)

                        await self.show_health(player, player.websocket)

                    # pause before attacking again
                    attack_time = False

    # respawn mobs after a certain amount of time
    async def respawn_mobs(self):
        while True:
            # Allow other tasks to complete
            await asyncio.sleep(2)

            # look through each room 
            for room in Rooms.rooms:
                # and if the room has monsters
                if len(room['monsters']) > 0:
                    for monster in room['monsters']:
                        # check if they're dead
                        if monster.is_alive == False:
                            current_epoch = int(time.time())

                            # if monster has been dead for more than monster.respawn_rate_secs, remove it and create new monster
                            # (we should consider making then kinda random (2-5 minutes for example))
                            secs_since_death = current_epoch - monster.dead_epoch
                            if secs_since_death >= monster.respawn_rate_secs:
                                # remove old monster
                                LogUtils.debug(f"Removing \"{monster.name}\" from room", logger)
                                room['monsters'].remove(monster)
                                
                                # create new monster
                                monsters = Monsters()
                                new_monster = await monsters.get_monster(monster.monster_type, room, logger)
                                LogUtils.info(f"Respawning \"{new_monster.name}\" in room {room['id']} ({room['name']})", logger)
                                room['monsters'].append(new_monster)

    # main loop when client connects
    async def main(self, websocket, path):
        # register client websockets - runs onces each time a new person starts
        player = await self.register(websocket)

        try:
            # setup world events
            await self.world.setup_world_events(logger)

            # start our mob combat task
            if self.world.mob_attack_task == None:
                self.world.mob_attack_task = asyncio.create_task(self.start_mob_combat())

            # start our resurrection task
            asyncio.create_task(self.respawn_mobs())

            # enter our player input loop
            while True:
                # send updated hp
                await self.show_health(player, websocket)

                # wait for a command to be sent
                LogUtils.info(f"Waiting for command...", logger)
                message = await websocket.recv()
                msg_obj = json.loads(message)

                if msg_obj["type"] == "cmd":
                    LogUtils.debug(f"Received: cmd", logger)
                    received_command = True
                    player, self.world = await Command.run_command(msg_obj["cmd"], player, self.world, websocket, logger)
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
