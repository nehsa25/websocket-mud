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
        return [
            RoomData(
                room_id=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                name="Town Square",
                description="You are in the town square...",
                environment_name=EnvironmentEnum.TOWNSMEE.name,
                monsters=[],
                items=[],
                npcs=[],
                characters=[],
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
                name="Inn",
                description="You find yourself within a majestic inn...",
                environment_name=EnvironmentEnum.TOWNSMEE.name,
                monsters=[],
                items=[],
                npcs=[],
                characters=[],
                exits=ExitData(
                    north=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_SHERIFF.value,
                name="Sheriff's Office",
                description="You are in the sheriff's office.",
                environment_name=EnvironmentEnum.TOWNSMEE.name,
                monsters=[],
                items=[],
                npcs=[],
                characters=[],
                exits=ExitData(
                    east=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_SHOP.value,
                name="Shop",
                description="You enter a bustling shop...",
                environment_name=EnvironmentEnum.TOWNSMEE.name,
                monsters=[],
                items=[],
                npcs=[],
                characters=[],
                exits=ExitData(
                    west=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                    southwest=RoomEnum.TOWNSMEE_MARKETPLACE.value
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_TAVERN.value,
                name="Tavern",
                description="The air is thick with the smell of ale and cheer...",                
                environment_name=EnvironmentEnum.TOWNSMEE.name,
                monsters=[],
                items=[],
                npcs=[],
                characters=[],
                exits=ExitData(
                    south=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                    west=RoomEnum.TOWNSMEE_INN.value,
                ),
                inside=True,
            ),
            RoomData(
                room_id=RoomEnum.TOWNSMEE_MARKETPLACE.value,
                name="Marketplace",
                description="Merchants hawk their wares in this open-air market.",                
                environment_name=EnvironmentEnum.TOWNSMEE.name,
                monsters=[],
                items=[],
                npcs=[],
                characters=[],
                exits=ExitData(
                    southwest=RoomEnum.TOWNSMEE_SHOP.value,
                    northwest=RoomEnum.TOWNSMEE_TOWNSQUARE.value,
                ),
                inside=False,
            ),
        ]