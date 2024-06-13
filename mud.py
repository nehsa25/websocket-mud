import ssl
import time
import asyncio
import websockets
import json
import traceback
import random
import sys
import inspect
from random import randint
from admin import Admin
from mudevent import MudWelcomeEvent
from utility import Utility
from command import Command
from player import Player
from log_utils import LogUtils, Level
from sysargs_utils import SysArgs
from world import World
from monsters import Monsters
from rooms import Rooms

class Mud:
    world = (
        World()
    )  # create our WORLD object that'll contain things like breeze and rain events
    COMBAT_WAIT_SECS = 3.5
    CHECK_FOR_MONSTERS_SECS = 2
    DEATH_RESPAWN_ROOM = 5
    REST_WAIT_SECS = 7
    worldName = "Illisurom"

    async def exit_handler(self, signal, frame):
        LogUtils.info("An exit signal as been received.  Exiting!", logger)
        # exit stuff..

    # shows color-coded health bar
    async def show_health(self, player, websocket):
        msg = f"{player.name}|{str(player.hitpoints)}/{str(player.max_hitpoints)}"
        if player.resting:
            msg += "|REST"
        await Utility.send_msg(msg, "health", websocket, logger)

    # shows inventory
    async def show_inventory(self, player, websocket):
        items = []
        for item in player.inventory:
            items.append(item.name)

        await Utility.send_msg(items, "inv", websocket, logger)

    # cancels all tasks and states you died if you die
    async def you_died(self, player, logger):
        # set combat to false
        player.in_combat = False

        # state you died
        await Utility.send_msg(
            "You die... but awaken on a strange beach shore.",
            "event",
            player.websocket,
            logger,
        )

        # alert others in the room where you died that you died..
        room = await self.world.get_room(player.location, logger)
        for p in room["players"]:
            if p != player:
                await Utility.send_msg(
                    f"{player.name} died.", "event", p.websocket, logger
                )

        # drop all items
        room = await self.world.get_room(player.location)
        for item in player.inventory:
            room["items"].append(item)
        player.inventory = []

        # set player location to beach shore
        player, self.world = await self.world.move_room(
            self.DEATH_RESPAWN_ROOM, player, self.world, player.websocket, logger
        )

        # alert others in the room that new player has arrived
        room = await self.world.get_room(self.DEATH_RESPAWN_ROOM, logger)
        for p in room["players"]:
            if p != player:
                await Utility.send_msg(
                    f"A bright purple spark floods your vision.  When it clears, {player.name} is standing before you.  Naked.",
                    "event",
                    p.websocket,
                    logger,
                )

        # set hits back to max / force health refresh
        player.hitpoints = player.max_hitpoints
        await self.show_health(player, player.websocket)

    # responsible for the "prepares to attack you messages"
    async def check_for_new_attacks(self, room, logger):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: Running...", logger)

        # for each monster in room still alive
        for monster in room["monsters"]:
            if monster.is_alive == True:
                LogUtils.debug(
                    f'{method_name}: Monster "{monster.name}" is alive', logger
                )

                # choose a player to attack each round
                current_combat = monster.in_combat

                if (
                    monster.in_combat == None
                ):  # if monster is not attacking anyone, just pick someone
                    monster.in_combat = random.choice(room["players"])
                    LogUtils.debug(
                        f'{method_name}: "{monster.name}" is not attacking anyone.  Now attacking {monster.in_combat.name}',
                        logger,
                    )
                elif (
                    monster.players_seen != room["players"]
                ):  # change combat if players enter/leave room
                    prev_combat = monster.in_combat
                    monster.in_combat = random.choice(room["players"])
                    monster.players_seen = room["players"].copy()
                    LogUtils.debug(
                        f"{method_name}: The players changed in room \"{room['name']}\".  \"{monster.name}\" was attacking {prev_combat.name}, now attacking: {monster.in_combat.name}",
                        logger,
                    )
                else:
                    LogUtils.debug(
                        f"{method_name}: Monster ({monster.name}) is in combat and nothing has changed in the room to switch combat...",
                        logger,
                    )

                # if the mob changed combat state, send message
                if monster.in_combat != current_combat:
                    LogUtils.debug(
                        f"{method_name}: Monster is changing combat: {monster.name}",
                        logger,
                    )

                    # cycle through all players
                    for p in room["players"]:
                        if monster.in_combat == p:
                            await Utility.send_msg(
                                f"{monster.name} prepares to attack you!",
                                "info",
                                p.websocket,
                                logger,
                            )

                            # stop resting
                            if p.resting == True:
                                p.resting = False
                                await Utility.send_msg(
                                    "You are no longer resting.",
                                    "info",
                                    p.websocket,
                                    logger,
                                )

                            for p2 in room["players"]:
                                if monster.in_combat != p2:
                                    await Utility.send_msg(
                                        f"{monster.name} prepares to attack {p.name}!",
                                        "info",
                                        p2.websocket,
                                        logger,
                                    )

                            # break out of loop
                            LogUtils.debug(
                                f"{method_name}: Breaking out of loop1", logger
                            )
                            break

    # calculate the round damage and sends messages to players
    async def calculate_mob_damage(self, player, room, logger):
        method_name = inspect.currentframe().f_code.co_name
        total_damage = 0
        monsters_damage = []
        monsters_in_room = False

        # need to check here if combat is still going.. we may have killed everything or moved rooms
        for monster in room["monsters"]:
            # as we call this function by player, we need to only capture damage by player
            if monster.is_alive == True and monster.in_combat == player:
                monsters_in_room = True
                LogUtils.debug(
                    f'{method_name}: Monster "{monster.name}" is alive and is attacking {player.name}!',
                    logger,
                )

                # calculate our damage
                obj = monster.damage.split("d")
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
        monsters_damage = sorted(
            monsters_damage, key=lambda k: k["damage"], reverse=True
        )

        # build our attack message
        attack_msg = ""
        print(f"\n\n\n{len(room['monsters'])}")
        if len(room["monsters"]) == 1:
            attack_msg = (
                f"{room['monsters'][0].name} hit you for {total_damage} damage!"
            )
        else:
            attack_msg = f"You were hit for {total_damage} damage!"
            attack_msg_extra = "("
            for monster_damage in monsters_damage:
                if monster_damage["damage"] > 0:
                    attack_msg_extra += (
                        f"{monster_damage['name']}: {monster_damage['damage']}, "
                    )
            attack_msg_extra = attack_msg_extra[0 : len(attack_msg_extra) - 2]
            attack_msg_extra += ")"
            attack_msg = f"{attack_msg} {attack_msg_extra}"

        # send our attack messages
        if monsters_in_room == True:
            for p in room["players"]:
                if p.websocket == player.websocket:
                    if total_damage > 0:
                        await Utility.send_msg(
                            f"{attack_msg}", "attack", p.websocket, logger
                        )
                    else:
                        await Utility.send_msg(
                            "You were dealt no damage this round!",
                            "info",
                            p.websocket,
                            logger,
                        )
                else:  # alert others of the battle
                    if total_damage > 0:
                        new_attack_msg = attack_msg.replace(
                            "You were", f"{player.name} was"
                        )
                        await Utility.send_msg(
                            new_attack_msg, "info", p.websocket, logger
                        )
                    else:
                        await Utility.send_msg(
                            f"{player.name} was dealt no damage!",
                            "info",
                            p.websocket,
                            logger,
                        )

        return total_damage

    # Determines round damage for each player
    async def apply_mob_round_damage(self, player, room, logger):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: Running...", logger)

        # determine damage
        total_damage = await self.calculate_mob_damage(player, room, logger)

        # update hp
        if total_damage > 0:
            player.hitpoints = player.hitpoints - total_damage

            # no point in continuing if player is dead..
            if player.hitpoints <= 0:
                await self.you_died(player, logger)

            # Updating health bar
            await self.show_health(player, player.websocket)

    # main loop for checking if monsters are attacking you
    async def mob_combat(self):
        method_name = inspect.currentframe().f_code.co_name

        # we never leave this attack loop
        while True:
            # for each player
            for player in self.world.players:
                LogUtils.debug(
                    f'{method_name}: On player "{player.name}", Running loop1...',
                    logger,
                )

                # get the room player is in
                room = await self.world.get_room(player.location, logger)
                LogUtils.debug(
                    f"{method_name}: Player \"{player.name}\" is in room \"{room['name']}\"",
                    logger,
                )

                # each monsters in room finds player to attack
                await self.check_for_new_attacks(room, logger)

            # sleep delay between rounds
            LogUtils.debug(
                f"{method_name}: Sleeping {str(self.COMBAT_WAIT_SECS)} seconds", logger
            )
            await asyncio.sleep(self.COMBAT_WAIT_SECS)

            for player in self.world.players:
                LogUtils.debug(
                    f'{method_name}: On player "{player.name}", Running loop2...',
                    logger,
                )

                # we need to get room again after we've slept
                room = await self.world.get_room(player.location, logger)

                # calculcate round damanage
                await self.apply_mob_round_damage(player, room, logger)

    # respawn mobs after a certain amount of time
    async def respawn_mobs(self):
        while True:
            # Allow other tasks to complete
            await asyncio.sleep(2)

            # look through each room
            rooms = Rooms().all_rooms
            for room in rooms:
                # and if the room has monsters
                if len(room["monsters"]) > 0:
                    for monster in room["monsters"]:
                        # check if they're dead
                        if monster.is_alive == False:
                            current_epoch = int(time.time())

                            # if monster has been dead for more than monster.respawn_rate_secs, remove it and create new monster
                            # (we should consider making then kinda random (2-5 minutes for example))
                            secs_since_death = current_epoch - monster.dead_epoch
                            if secs_since_death >= monster.respawn_rate_secs:
                                # remove old monster
                                LogUtils.debug(
                                    f'Removing "{monster.name}" from room', logger
                                )
                                room["monsters"].remove(monster)

                                # create new monster
                                monsters = Monsters()
                                new_monster = await monsters.get_monster(
                                    monster.monster_type, room, logger
                                )
                                LogUtils.info(
                                    f"Respawning \"{new_monster.name}\" in room {room['id']} ({room['name']})",
                                    logger,
                                )
                                room["monsters"].append(new_monster)

    # increases hp when resting
    async def check_for_resting(self, websocket, player):
        while True:
            # Check resting every 2 seconds
            await asyncio.sleep(self.REST_WAIT_SECS)

            if player.resting == True:
                LogUtils.debug("Checking if resting...", logger)
                if player.hitpoints < player.max_hitpoints:
                    heal = randint(1, 3)
                    if heal == 1:
                        await Utility.send_msg(
                            f"You recover {heal} hitpoint.",
                            "info",
                            player.websocket,
                            logger,
                        )
                    else:
                        await Utility.send_msg(
                            f"You recover {heal} hitpoints.",
                            "info",
                            player.websocket,
                            logger,
                        )
                    player.hitpoints += 3
                    if player.hitpoints >= player.max_hitpoints:
                        player.hitpoints = player.max_hitpoints
                        player.resting = False
                        await Utility.send_msg(
                            "You have fully recovered.",
                            "info",
                            player.websocket,
                            logger,
                        )

                    await self.show_health(player, player.websocket)

    # main loop when client connects
    async def main(self, websocket, path):
        # register client websockets - runs onces each time a new person starts
        player, self.world = await Admin.new_user(self.world, websocket, logger)

        try:
            # setup world events
            await self.world.setup_world_events(logger)

            if self.world.mob_attack_task == None:
                self.world.mob_attack_task = asyncio.create_task(self.mob_combat())

            # start our resurrection task
            asyncio.create_task(self.respawn_mobs())

            # start our resting task
            asyncio.create_task(self.check_for_resting(websocket, player))

            # enter our player input loop
            while True:
                # set inventory for refresh
                await self.show_inventory(player, player.websocket)

                # calculate rest
                # TODO

                # send updated hp
                await self.show_health(player, websocket)

                # wait for a command to be sent
                LogUtils.info(f"Waiting for command...", logger)
                message = await websocket.recv()
                msg_obj = json.loads(message)
                extra_data = None

                if msg_obj["type"] == "cmd":
                    LogUtils.debug(f"Received: " + json.dumps(msg_obj), logger)
                    if msg_obj["extra"] != None:
                        extra_data = msg_obj["extra"]
                        
                    player, self.world = await Command.run_command(
                        msg_obj["cmd"], player, self.world, websocket, logger, extra_data
                    )
                else:
                    LogUtils.error(f"Received unknown message: {message}", logger)
        except KeyboardInterrupt:
            loop.stop()
        except:
            LogUtils.error(
                f"An error occurred!\nException:\n{traceback.format_exc()}", logger
            )
        finally:
            await Admin.unregister(self.world, websocket, logger)


if __name__ == "__main__":
    try:
        # logger = LogUtils.get_logger(filename='mud.log', file_level=Level.DEBUG, console_level=Level.DEBUG, log_location="d:\\src\\mud", logger_name='websockets')
        logger = LogUtils.get_logger(
            filename="mud.log",
            file_level=Level.DEBUG,
            console_level=Level.DEBUG,
            log_location="c:\\src\\websocket-mud",
        )
        m = Mud()

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
