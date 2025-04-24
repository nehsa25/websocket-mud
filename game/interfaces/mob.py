from abc import abstractmethod


class MOBInterface:
    name = ""
    title = ""
    description = ""
    common_phrases = []
    interests = []
    schedules = []
    wander_event = None
    last_direction = None
    wanders = False
    room_id = None
    prev_room_id = None
    last_check_combat = None
    alignment = None
    in_combat = False

    # announce we're here!
    @abstractmethod
    async def announce_entrance(self, room) -> None:
        pass

    @abstractmethod
    async def stop_combat(self, player):
        pass

    @abstractmethod
    async def break_combat(self, room):
        pass
    
    @abstractmethod
    async def killed(self, room):
        pass

    @abstractmethod
    async def respawn(self, world_state):
        pass

    @abstractmethod
    async def wander(self, world_state, is_npc):
        pass

    @abstractmethod
    async def check_combat(self, world_state):
        pass

    @abstractmethod
    async def speak(self, room, world_state):
        pass

    @abstractmethod
    async def move(self, direction, world_state, isNpc=True):
        pass
