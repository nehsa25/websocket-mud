import asyncio
from random import randint
from utility import Utility

class World:
    # players
    players = []

    breeze_task = None
    rain_task = None
    eerie_task = None
    thunder_task = None

    # It begins to rain..
    async def rain(self, websocket, logger):
        while True:
            rand = randint(2000, 3600*2)
            await asyncio.sleep(rand)
            await Utility.send_msg("It begins to rain..", 'event', websocket, logger)

            # wait for it to stop
            rand = randint(100, 500)
            await asyncio.sleep(rand)
            await Utility.send_msg("The rain pitter-patters to a stop and the sun begins to shine through the clouds..", 'event', websocket, logger)

    # You hear thunder off in the distane..
    async def thunder(self, websocket, logger):
        while True:
            rand = randint(2000, 3800*2)
            await asyncio.sleep(rand)
            await Utility.send_msg("You hear thunder off in the distance..", 'event', websocket, logger)

    # A gentle breeze blows by you..
    async def breeze(self, websocket, logger):        
        while True:
            rand = randint(2000, 3800*2)
            await asyncio.sleep(rand)
            await Utility.send_msg("A gentle breeze blows by you..", 'event', websocket, logger)

    # An eerie silence settles on the room..
    async def eerie_silence(self, websocket, logger):
        while True:
            rand = randint(2000, 4000*2)
            await asyncio.sleep(rand)
            await Utility.send_msg("An eerie silence settles on the room..", 'event', websocket, logger)
