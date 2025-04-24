from abc import abstractmethod


class PlayerInterface:
    @abstractmethod
    async def check_combat(self, room):
        pass

    @abstractmethod
    async def break_combat(self, room):
        pass

    @abstractmethod
    async def attack(self, room):
        pass

    @abstractmethod
    async def speak(self, room, world_state):
        pass

    @abstractmethod
    async def move(self, direction, world_state, isNpc=True):
        pass

    @abstractmethod
    async def get_hp(self, room):
        pass

    async def get_hp_description(self):
        pass

    @abstractmethod
    async def get_intelligence(self):
        pass

    @abstractmethod
    async def get_intelligence_description(self):
        pass

    @abstractmethod
    async def get_strength(self):
        pass

    @abstractmethod
    async def get_strength_description(self):
        pass

    @abstractmethod
    async def get_dexterity(self):
        pass

    @abstractmethod
    async def get_dexterity_description(self):
        pass

    @abstractmethod
    async def get_constitution(self):
        pass

    @abstractmethod
    async def get_constitution_description(self):
        pass

    @abstractmethod
    async def get_faith(self):
        pass
    
    @abstractmethod
    async def get_faith_description(self):
        pass

    @abstractmethod
    async def get_charisma(self):
        pass

    @abstractmethod
    async def get_charisma_description(self):
        pass

    @abstractmethod
    async def get_experience(self):
        pass

    @abstractmethod
    async def get_level(self):
        pass

    @abstractmethod
    async def get_age(self):
        pass

    @abstractmethod
    async def rest(self, rest: bool):
        pass

    @abstractmethod
    async def die(self, world):
        pass

    @abstractmethod
    async def get_inventory(self):
        pass

    @abstractmethod
    async def check_rest(self):
        pass

    @abstractmethod
    async def get_description(self):
        pass
