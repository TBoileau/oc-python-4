"""Imported modules/packages"""
from abc import ABC
from typing import Dict

from src.entity.player import Player


class PlayerFactoryInterface(ABC):
    """
    Player factory interface
    """

    def create(self, data: Dict) -> Player:
        """
        Create an instance of Player

        :param data:
        :return:
        """
