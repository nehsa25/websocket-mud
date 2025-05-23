from core.enums.send_scope import SendScopeEnum
from core.events.info import InfoEvent


class MOBHelper:
    async def equip(self, player, action_eq=True):
        self.logger.debug("enter")
        if not self.can_be_equipped and action_eq is True:
            await self.world.self.world.utility.send_msg(
                f"You cannot wield {self.name}.", "info", player.websocket, self.logger
            )
            return

        if action_eq is True and self.equipped is False:
            self.equipped = True
            await InfoEvent(f"You wield {self.name}.").send(player.websocket)
            await InfoEvent(
                f"You notice {player.selected_character.name} equip {self.name}.",
                exclude_player=True,
                scope=SendScopeEnum.ROOM,
            ).send(player.websocket)

        if action_eq is False and self.equipped is True:
            self.equipped = False
            await InfoEvent(f"You unequip {self.name}.").send(player.websocket)
            await InfoEvent(f"You notice {player.selected_character.name} unequip {self.name}.").send(
                player.websocket, exclude_player=True, scope=SendScopeEnum.ROOM
            )
        self.logger.debug("exit")

    async def get(self, player, action_get=True):
        pass

    async def drop(self, player, action_drop=True):
        pass
