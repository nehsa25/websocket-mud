from typing import Dict


class DirectiveData:
    directive: str
    def __init__(self, directive = []):
        self.directive = directive

    def __str__(self):
        return self.name

    def to_dict(self) -> Dict:
        """Helper method to convert Class to a dictionary."""
        return {
            "directive": self.directive
        }