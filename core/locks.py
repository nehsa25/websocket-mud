import asyncio


class NpcLock:
    npc = None
    lock = None

    def __init__(self, npc):
        self.npc = npc
        self.lock = asyncio.Lock()
