from core.game_objects.game_item import GameItem
from utilities.log_telemetry import LogTelemetryUtility


class FoodItem(GameItem):
    name = None
    damage_potential = None
    weight_class = None
    item_type = None
    verb = None
    plural_verb = None
    equipped = False
    can_be_equipped = False
    description = None
    contents = None
    logger = None

    def __init__(
        self,
        name,
        item_type,
        damage_potential,
        weight_class,
        verb,
        plural_verb,
        description,
        contents=None,
    ):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing FoodItem() class")
        self.name = name
        self.damage_potential = damage_potential
        self.weight_class = weight_class
        self.item_type = item_type
        self.verb = verb
        self.plural_verb = plural_verb
        self.description = description
        self.contents = contents

    async def equip(self, player, action_eq=True):
        self.logger.debug("enter")
        if not self.can_be_equipped and action_eq is True:
            await self.world.self.world.utility.send_msg(
                f"You cannot wield {self.name}.", "info", player.websocket, self.logger
            )
            return

        if action_eq is True and self.equipped is False:
            self.equipped = True
            await self.world.self.world.utility.send_msg(
                f"You wield {self.name}.", "info", player.websocket, self.logger
            )
            await player.room.alert(
                f"You notice {player.name} equip {self.name}.",
                exclude_player=True,
                player=player,
            )

        if action_eq is False and self.equipped is True:
            self.equipped = False
            await self.world.self.world.utility.send_msg(
                f"You unequip {self.name}.", "info", player.websocket, self.logger
            )
            await player.room.alert(
                f"You notice {player.name} unequip {self.name}.",
                exclude_player=True,
                player=player,
            )

        self.logger.debug("exit")
