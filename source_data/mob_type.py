from core.data.mob_type_data import MobTypeData
from core.enums.mob_types import MobTypeEnum
from core.interfaces.source_data import SourceInterface


class MobTypeSource(SourceInterface):
    """
    This class is used to represent the source data for MobTypeSource for
    initalization of the database.
    """

    def get_data(self):
        return [
            MobTypeData(
                type=MobTypeEnum.PLAYER.value,
                description="A player character, a real person. You.",
            ),
            MobTypeData(
                type=MobTypeEnum.MONSTER.value,
                description="A monster, a creature that fights based on its alignment against yours (if it's evil and you are good, it will attack you).",
            ),
            MobTypeData(
                type=MobTypeEnum.NPC.value,
                description="A non-player character, able to trade and talk.",
            ),
            MobTypeData(
                type=MobTypeEnum.PET.value,
                description="A pet, a creature that is tamed and follows you around.",
            ),
        ]
