# interfaces/direction_interface.py
from abc import ABC, abstractmethod
from typing import Dict


class SourceInterface(ABC):
    """ Populating database """

    @abstractmethod
    def get_data(self) -> Dict:
        pass
