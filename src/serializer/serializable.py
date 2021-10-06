"""Imported modules/packages"""
from abc import ABC
from typing import Dict, Any


class Serializable(ABC):
    """
    Serializable interface
    """

    def serialize(self) -> Dict[str, Any]:
        """
        Return serialized data

        :return:
        """
