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

    async def get(self, player, action_get=True):
        pass

    async def drop(self, player, action_drop=True):
        pass
