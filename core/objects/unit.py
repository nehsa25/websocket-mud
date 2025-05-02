import time
from core.data.body_stats_data import BodyStatsData
from utilities.log_telemetry import LogTelemetryUtility


class UnitTypes:
    logger = None

    def __init__(self) -> None:
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.info("Initializing UnitTypes() class")

    class NPC(BodyStatsData):
        logger = None

        def __init__(self):
            self.logger = LogTelemetryUtility.get_logger(__name__)
            self.logger.info("Initializing NPC() class")

    class Monster(BodyStatsData):
        logger = None

        def __init__(self):
            self.logger.info("Initializing Monster() class")


class Unit(UnitTypes):
    name = None
    description = None
    type = None
    hp = None
    strength = None
    agility = None
    perception = None
    wanders = None
    logger = None

    def __init__(self):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing Unit() class")

    def generate_unit(
        self, title, name, hp, strength, agility, perception, description, wanders=False
    ):
        self.logger.debug("enter")
        self.name = name
        self.title = title
        self.hp = hp
        self.strength = strength
        self.agility = agility
        self.perception = perception
        self.description = description
        self.wanders = wanders
        self.logger.debug("exit")
        return self

    # uses speed of unit
    # executor.submit(self.ut.move_unit_over_time, self.pgu, self.grid, army_unit, mouse_pos[0], mouse_pos[1]))
    def move_unit_over_time(self, path):
        self.logger.debug("enter")
        previousStep = None
        default_speed = 0.35  # higher is faster?
        speed = default_speed - (self.type.speed * 0.1)
        for step in path:
            self.logger.debug(
                f"Sleeping: {round(speed, 2)} seconds before moving {self.name} again ({self})"
            )
            time.sleep(speed)
            if previousStep is None:
                self.logger.debug(
                    f"{self.name} beginning travel to {path[len(path) - 1]})"
                )
            else:
                self.logger.debug(f"Moving {self.name} from {previousStep} to {step}")
            previousStep = step
        self.RectSettings.Rect = previousStep
        self.move_thread = False
        self.logger.debug("exit")
