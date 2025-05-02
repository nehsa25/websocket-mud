from utilities.log_telemetry import LogTelemetryUtility


class GameItem:
    name = None
    damage_potential = None
    weight_class = None
    item_type = None
    verb = None
    plural_verb = None
    equipped = False
    can_be_equipped = False
    description = None
    contents = None
    logger = None

    def __init__(
        self,
        name,
        item_type,
        damage_potential,
        weight_class,
        verb,
        plural_verb,
        description,
        contents=None,
    ):
        self.logger = LogTelemetryUtility.get_logger(__name__)
        self.logger.debug("Initializing GameItem() class")
        self.name = name
        self.damage_potential = damage_potential
        self.weight_class = weight_class
        self.item_type = item_type
        self.verb = verb
        self.plural_verb = plural_verb
        self.description = description
        self.contents = contents
