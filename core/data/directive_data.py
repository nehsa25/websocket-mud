from typing import Dict


class DirectiveData:
    directive: str
    directive_type: str

    def __init__(self, directive, directive_type):
        self.directive = directive
        self.directive_type = directive_type

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "directive": self.directive,
            "directive_type": self.directive_type,
        }