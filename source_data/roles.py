from core.data.role import RoleData
from core.enums.roles import RoleEnum
from core.interfaces.source_data import SourceInterface


class RoleSource(SourceInterface):
    """
    This class is used to represent the source data for roles for
    initalization of the database.
    """

    def get_data(self):
        return [
            RoleData(
                name=RoleEnum.ADMIN.value,
                description="Full rights",
            ),
            RoleData(
                name=RoleEnum.MODERATOR.value,
                description="Access to moderator commands",
            ),
                RoleData(
                name=RoleEnum.USER.value,
                description="Standard user role",
            ),
        ]