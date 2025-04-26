
class DirectiveData:
    brightness = int

    def __init__(
        self,
        name,
        item_type,
        weight,
        verb,
        plural_verb,
        description,
        quality,
        brightness,
    ):
        super().__init__(
            name,
            item_type,
            weight,
            verb,
            plural_verb,
            description,
            quality,
        )
        self.defences = brightness
