"""Imported modules/packages"""
from abc import ABC
from typing import Dict

from src.entity.match import Match


class MatchFactoryInterface(ABC):
    """
    Match factory interface
    """

    def create(self, data: Dict) -> Match:
        """
        Create an instance of Match

        :param data:
        :return:
        """
