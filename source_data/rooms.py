from core.data.room_data import RoomData
from core.interfaces.source_data import SourceInterface
from settings.world_settings import WorldSettings


class RoomSource(SourceInterface):
    """
    This class is used to represent the source data for monsters for
    initalization of the database.
    """

    def get_data(self):
        return [
            RoomData(
                name=f"{WorldSettings.WORLD_NAME} - Town Square",
                description="You are in the town square...",
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=[],
                inside=False,
            ),
            RoomData(
                name=f"{WorldSettings.WORLD_NAME} - Inn",
                description="You find yourself within a majestic inn...",
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=[],
                inside=True,
            ),
            RoomData(
                name=f"{WorldSettings.WORLD_NAME} - Sheriff's Office",
                description="You are in the sheriff's office.",
                monsters=[],
                items=[],
                npcs=[],
                players=[],
                exits=[],
                inside=True,
            ),
        ]
