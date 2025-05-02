from core.data.environment_data import EnvironmentData
from core.enums.environments import EnvironmentEnum
from core.interfaces.source_data import SourceInterface


class EnvironmentsSource(SourceInterface):
    """
    This class is used to represent the source data for environments in the world for
    initalization of the database.
    """

    def get_data(self):
        return [
            EnvironmentData(
                name=EnvironmentEnum.TOWNSMEE.value,
                description="Starting town",
                spawn_monsters=False,
                spawn_guards=True,
            ),
            EnvironmentData(
                name=EnvironmentEnum.UNDERWORLD.value,
                description="The underworld.",
                spawn_monsters=False,
                spawn_guards=True,
            ),
            EnvironmentData(
                name=EnvironmentEnum.CAVES.value,
                description="A series of dark caves.",
                spawn_monsters=False,
                spawn_guards=True,
            ),
            EnvironmentData(
                name=EnvironmentEnum.GRAVEYARD.value,
                description="Graveyard",
                spawn_monsters=True,
                spawn_guards=False,
            ),
            EnvironmentData(
                name=EnvironmentEnum.BREACH.value,
                description="An otherworldly breach into another dimension.",
                spawn_monsters=True,
                spawn_guards=False,
            ),
            EnvironmentData(
                name=EnvironmentEnum.BEACH.value,
                description="Along the shore of the ocean.",
                spawn_monsters=True,
                spawn_guards=False,
            ),
            EnvironmentData(
                name=EnvironmentEnum.KINGSFOREST.value,
                description="Forest environment with trees and wildlife, near castle",
                spawn_monsters=True,
                spawn_guards=False,
            ),
            EnvironmentData(
                name=EnvironmentEnum.DARKFOREST.value,
                description="The absense of all light makes this forest dark and foreboding. The trees are twisted and gnarled, their branches reaching out like skeletal fingers.",
                spawn_monsters=True,
                spawn_guards=False,
            ),
            EnvironmentData(
                name=EnvironmentEnum.REDFOREST.value,
                description="Forest environment with trees and wildlife. The semi-translucent leaves of the trees wash the ground in a soft reddish light. It's eerie.",
                spawn_monsters=True,
                spawn_guards=False,
            ),
            EnvironmentData(
                name=EnvironmentEnum.SMEEUNIVERSITY.value,
                description="A place of learning and knowledge.",
                spawn_monsters=True,
                spawn_guards=False,
            ),
        ]
