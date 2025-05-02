from core.data.alignments_data import AligntmentsData
from core.enums.alignments import AlignmentEnum
from core.interfaces.source_data import SourceInterface


class AlignmentsSource(SourceInterface):
    """
    This class is used to represent the source data for alignment data in the world for
    initalization of the database.
    """

    def get_data(self):
        return [
            AligntmentsData(
                name=AlignmentEnum.LAWFUL_GOOD.value,
                description="Attacks evil players only and only if attacked first.",
            ),
            AligntmentsData(name=AlignmentEnum.GOOD.value, description="Attacks evil players only."),
            AligntmentsData(name=AlignmentEnum.NEUTRAL.value, description="Only attacks if attacked."),
            AligntmentsData(name=AlignmentEnum.EVIL.value, description="Attacks everyone."),
        ]
