from core.data.exit_data import ExitData
from core.data.room_data import RoomData
from core.enums.environments import EnvironmentEnum
from core.enums.rooms import RoomEnum
from core.interfaces.source_data import SourceInterface
class RoomSource(SourceInterface):
    """
    This class is used to represent the source data for rooms for
    initalization of the database.
    """

    def get_data(self):
        environment_name = EnvironmentEnum.TOWNSMEE.value
        return [
            RoomData(
                room_id=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                name=f"{environment_name} - Town Square",
                description="You are in the town square...",
                environment=environment_name,
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=ExitData(
                    north=RoomEnum.TOWNSMEE_TAVERN.value,
                    south=RoomEnum.TOWNSMEE_INN.value,
                    east=RoomEnum.TOWNSMEE_SHOP.value,
                    west=RoomEnum.TOWNSMEE_SHERIFF.value,
                    northeast=RoomEnum.TOWNSMEE_MARKETPLACE.value,
                ),
                inside=False,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_INN.value,
                name=f"{environment_name} - Inn",
                description="You find yourself within a majestic inn...",
                environment=environment_name,
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=ExitData(
                    north=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_SHERIFF.value,
                name=f"{environment_name} - Sheriff's Office",
                description="You are in the sheriff's office.",
                environment=environment_name,
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=ExitData(
                    east=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_SHOP.value,
                name=f"{environment_name} - Shop",
                description="You enter a bustling shop...",
                environment=environment_name,
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=ExitData(
                    west=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                    southwest=RoomEnum.TOWNSMEE_MARKETPLACE.value
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_TAVERN.value,
                name=f"{environment_name} - Tavern",
                description="The air is thick with the smell of ale and cheer...",
                environment=environment_name,
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=ExitData(
                    south=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                    west=RoomEnum.TOWNSMEE_INN.value,
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_MARKETPLACE.value,
                name=f"{environment_name} - Marketplace",
                description="Merchants hawk their wares in this open-air market.",
                environment=environment_name,
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=ExitData(
                    southwest=RoomEnum.TOWNSMEE_SHOP.value,
                    northwest=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                ),
                inside=False,
            ),
        ]