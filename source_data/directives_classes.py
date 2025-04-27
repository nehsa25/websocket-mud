from core.data.directive_data import DirectiveData
from core.enums.directive_types import DirectiveTypeEnum
from core.enums.directives import DirectiveEnum
from core.interfaces.source_data import SourceInterface


class DirectivesClassesSource(SourceInterface):
    """
    This class is used to represent the source data for npc and monster behavior directives for
    initalization of the database.
    """

    def get_data(self):
        return [
            DirectiveData(
                directive=DirectiveEnum.LOW_THIEF.value,
                directive_type=DirectiveTypeEnum.BEHAVIOR.value
            ),
        ]
