import inspect
import json
from random import randint
import random
from websockets import ConnectionClosedOK
from player_classes.barbarian import Barbarian
from player_classes.bard import Bard
from player_classes.battle_mage import BattleMage
from player_classes.berserker import Berserker
from player_classes.bowman import Bowman
from player_classes.cleric import Cleric
from player_classes.druid import Druid
from player_classes.illusionist import Illusionist
from player_classes.knight import Knight
from player_classes.mage import Mage
from player_classes.monk import Monk
from player_classes.necromancer import Necromancer
from player_classes.paladin import Paladin
from player_classes.ranger import Ranger
from player_classes.rogue import Rogue
from player_classes.sorcerer import Sorcorer
from player_classes.warlock import Warlock
from player_classes.warrior import Warrior
from races.goblin import Goblin
from races.orc import Orc
from races.arguna import Arguna
from races.earea import Earea
from races.elf import Elf
from races.fae import Fae
from races.halfling import Halfing
from races.halfogre import HalfOgre
from races.human import Human
from inventory import Inventory
from items import Items
from races.kobold import Kobold
from log_utils import LogUtils
from money import Money
from mudevent import MudEvents
from races.nyrriss import Nyrriss
from player import Player
from utility import Utility
from wordsmith import Pronouns

class Players(Utility):
    logger = None
    players = []

    def __init__(self, logger) -> None:
        self.logger = logger
        LogUtils.debug("Initializing Players() class", self.logger)

    # used to update webpage on user count
    async def update_website_users_online(self, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        get_client_event = world_state.players.GetClientEvent(len(self.players))
        for player in self.players:
            await self.send_message(get_client_event, player.websocket)
        LogUtils.debug(f"{method_name}: exit", self.logger)

    async def register(self, player, world_state):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter, player: {player.name}", self.logger)

        # if the name is already taken, request another
        matching_players = [p for p in self.players if p.name == player.name]
        if matching_players != []:
            LogUtils.debug(
                f"Name ({matching_players[0].name}) is already taken, requesting a different one..",
                self.logger,
            )
            await self.new_user(world_state, player.websocket, dupe=True)

        self.players.append(player)
        await self.update_website_users_online(world_state)

        # send msg to everyone
        for p in self.players:
            if p.name == player.name:
                await self.send_message(
                    MudEvents.WelcomeEvent(f"Welcome {player.name}!"), p.websocket
                )
            else:
                await self.send_message(
                    MudEvents.AnnouncementEvent(f"{player.name} joined the game!"),
                    p.websocket,
                )
        LogUtils.debug(f"{method_name}: exit", self.logger)

        return player, world_state

    # calls at the beginning of the connection.  websocket connection here is the real connection
    async def new_user(self, world_state, websocket, dupe=False):
        try:
            method_name = inspect.currentframe().f_code.co_name
            LogUtils.debug(
                f"{method_name}: enter, duplicate user flow: {dupe}", self.logger
            )
            LogUtils.info(f"{method_name}: {websocket.remote_address}", self.logger)
            ip = websocket.remote_address[0]
            LogUtils.info(
                f"A new user has connected to NehsaMUD from {ip}", self.logger
            )

            # get the client hostname
            LogUtils.info(f"Requesting username", self.logger)
            if dupe:
                await self.send_message(MudEvents.DuplicateNameEvent(), websocket)
            else:
                await self.send_message(
                    MudEvents.UsernameRequestEvent(Utility.Share.WORLD_NAME), websocket
                )
            LogUtils.info(f"Awaiting client name response from client..", self.logger)
            msg = await websocket.recv()
            LogUtils.info(f"Message received: {msg}", self.logger)
            request = json.loads(msg)
            player_race = random.choice(list(Utility.Share.Races))
            player_class = random.choice(list(Utility.Share.Classes)).name
            player_intelligence = randint(1, 50)
            player_hp = randint(1, 50)
            player_strength = randint(1, 50)
            player_agility = randint(1, 50)
            player_location = randint(1, 10)
            player_perception = randint(1, 50)
            player_faith = randint(1, 50)
            player_determination = randint(1, 50)
            age = randint(1, 75)
            level = randint(1, 75)
            pronoun = random.choice(list(Pronouns))
            
            if player_class == Utility.Share.Classes.MAGE.name:
                player_class = Mage(self.logger)
            elif player_class == Utility.Share.Classes.BATTLE_MAGE.name:
                player_class = BattleMage(self.logger)
            elif player_class == Utility.Share.Classes.WARLOCK.name:
                player_class = Warlock(self.logger)
            elif player_class == Utility.Share.Classes.WARRIOR.name:
                player_class = Warrior(self.logger)
            elif player_class == Utility.Share.Classes.ROGUE.name:
                player_class = Rogue(self.logger)
            elif player_class == Utility.Share.Classes.PALADIN.name:
                player_class = Paladin(self.logger)
            elif player_class == Utility.Share.Classes.RANGER.name:
                player_class = Ranger(self.logger)
            elif player_class == Utility.Share.Classes.BARD.name:
                player_class = Bard(self.logger)
            elif player_class == Utility.Share.Classes.DRUID.name:
                player_class = Druid(self.logger)
            elif player_class == Utility.Share.Classes.CLERIC.name:
                player_class = Cleric(self.logger)
            elif player_class == Utility.Share.Classes.SORCERER.name:
                player_class = Sorcorer(self.logger)
            elif player_class == Utility.Share.Classes.BARBARIAN.name:
                player_class = Barbarian(self.logger)
            elif player_class == Utility.Share.Classes.MONK.name:
                player_class = Monk(self.logger)
            elif player_class == Utility.Share.Classes.PALADIN.name:
                player_class = Paladin(self.logger)
            elif player_class == Utility.Share.Classes.NECROMANCER.name:
                player_class = Necromancer(self.logger)
            elif player_class == Utility.Share.Classes.ILLUSIONIST.name:
                player_class = Illusionist(self.logger)
            elif player_class == Utility.Share.Classes.KNIGHT.name:
                player_class = Knight(self.logger)
            elif player_class == Utility.Share.Classes.BOWMAN.name:
                player_class = Bowman(self.logger)
            elif player_class == Utility.Share.Classes.BERSERKER.name:
                player_class = Berserker(self.logger)

            if player_race == Utility.Share.Races.ARGUNA:
                player_race = Arguna(self.logger)
            elif player_race == Utility.Share.Races.EAREA:
                player_race = Earea(self.logger)
            elif player_race == Utility.Share.Races.HALFLING:
                player_race = Halfing(self.logger)
            elif player_race == Utility.Share.Races.HUMAN:
                player_race = Human(self.logger)
            elif player_race == Utility.Share.Races.NYRRISS:
                player_race = Nyrriss(self.logger)
            elif player_race == Utility.Share.Races.ORC:
                player_race = Orc(self.logger)
            elif player_race == Utility.Share.Races.KOBOLD:
                player_race = Kobold(self.logger)
            elif player_race == Utility.Share.Races.ELF:
                player_race = Elf(self.logger)
            elif player_race == Utility.Share.Races.FAE:
                player_race = Fae(self.logger)
            elif player_race == Utility.Share.Races.HALFOGRE:
                player_race = HalfOgre(self.logger)
            elif player_race == Utility.Share.Races.GOBLIN:
                player_race = Goblin(self.logger) 

            inventory = Inventory(
                items=[Items.club, Items.book, Items.cloth_pants], money=Money(1000001)
            )
            player = Player(
                name=request["username"],
                level = level,
                race=player_race,
                pronoun=pronoun,
                age=age,
                player_class=player_class,
                intelligence=player_intelligence,
                hp=player_hp,
                strength=player_strength,
                agility=player_agility,
                location_id=player_location,
                perception=player_perception,
                determination=player_determination,
                faith=player_faith,
                inventory=inventory,
                ip=ip,
                websocket=websocket,
                logger=self.logger,
            )

            if request["type"] == MudEvents.EventUtility.get_event_type_id(
                MudEvents.EventUtility.EventTypes.USERNAME_ANSWER
            ):
                await self.register(player, world_state)

                # move player to initial room
                world_state = await world_state.move_room_player(
                    player.location_id, player
                )
                
                # send initial status
                await player.send_status()
            else:
                raise Exception(f"Shananigans? received request: {request['type']}")

            LogUtils.debug(f"{method_name}: exit", self.logger)
            return world_state
        except ConnectionClosedOK:
            LogUtils.warn(f"ConnectionClosedOK ({player.name} left).", self.logger)
        except Exception as e:
            raise Exception(f"An error occurred during new_user(): {e}")

    # called when a client disconnects
    async def unregister(self, player, world_state, change_name=False):
        LogUtils.debug(f"unregister: enter, player: {player.name}", self.logger)
        LogUtils.debug(f"self.players count: {len(self.players)}", self.logger)
        self.players = [i for i in self.players if not i.websocket == player.websocket]
        await self.update_website_users_online(world_state)

        # let folks know someone left
        if change_name:
            await world_state.alert_world(
                f"{player.name} is changing their name..", player=player
            )
        else:
            await world_state.alert_world(
                f"{player.name} left the game.", player=player
            )

        LogUtils.info(f"new player count: {len(self.players)}", self.logger)
        LogUtils.debug(f"register: exit", self.logger)

    async def get_player(self, websocket):
        method_name = inspect.currentframe().f_code.co_name
        LogUtils.debug(f"{method_name}: enter", self.logger)
        player = None
        if self.players == []:
            return player

        for p in self.players:
            if p.websocket == websocket:
                player = p
                break
        LogUtils.debug(f"{method_name}: exit, returning: {player.name}", self.logger)
        return player
