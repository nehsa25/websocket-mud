from class_types.directive_type import DirectiveType
from game.enums.directive_types import DirectiveTypes
from game.enums.directives import Directives
from game.interfaces.source_data import SourceInterface


class DirectivesSource(SourceInterface):
    """
    This class is used to represent the source data for npc and monster behavior directives for
    initalization of the database.
    """

    def get_data(self):
        return [
            DirectiveType(
                directive_type=DirectiveTypes.BEHAVIOR.value,
                value=Directives.LOW_THIEF.value,
            ),
        ]
