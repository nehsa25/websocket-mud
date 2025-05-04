from core.enums.send_scope import SendScopeEnum
from core.events.error import ErrorEvent
from core.events.info import InfoEvent
from utilities.log_telemetry import LogTelemetryUtility
from utilities.money import MoneyUtility


class Inventory:
    items = []
    money = None

    def __init__(self, items=[], money=MoneyUtility()):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Inventory() class")
        self.items = items
        self.money = money

    async def get_item(self, wanted_item, player):
        self.logger.debug("enter")
        found = False
        for item in player.room.items:
            if wanted_item != item.name.lower():
                continue

            found = True

            # send message to player
            await InfoEvent(f"You pick up {item.name}.").send(player.websocket)
            await InfoEvent(f"{player.name} picks up {wanted_item}.").send(
                player.websocket, exclude_player=True, scope=SendScopeEnum.ROOM
            )

            # add item to inventory
            self.items.append(item)
            await player.send_inventory()
            break

        if not found:
            await ErrorEvent(
                f"{wanted_item} is not a valid loot target.",
                exclude_player=True,
            ).send(player.websocket)

        self.logger.debug("exit")

    async def drop_item(self, wanted_item, player):
        self.logger.debug("enter")
        found = False
        for item in player.room.items:
            if wanted_item != item.name.lower():
                continue

            found = True

            # send message to player
            await InfoEvent(f"You drop {item.name}.").send(player.websocket)
            await InfoEvent(f"{player.name} drops {wanted_item}.").send(
                player.websocket,
                exclude_player=True,
                scope=SendScopeEnum.ROOM
            )

            # add item to inventory
            self.items.remove(item)
            await player.send_inventory()
            break

        if not found:
            await ErrorEvent(f"You do not have {wanted_item}.").send(player.websocket)

        self.logger.debug("exit")
