"""Imported modules/packages"""
from abc import ABC
from datetime import date
from typing import Dict
from uuid import UUID

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


class PlayerFactory(PlayerFactoryInterface):
    """
    Player factory
    """

    def create(self, data: Dict) -> Player:
        return Player(
            UUID(data["id"]),
            data["last_name"],
            data["first_name"],
            date.fromisoformat(data["birthday"]),
            data["gender"],
            int(data["ranking"]),
        )
