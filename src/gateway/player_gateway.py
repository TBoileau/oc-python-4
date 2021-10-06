"""Imported modules/packages"""
from abc import ABC
from typing import List, Optional

from src.entity.player import Player


class PlayerGateway(ABC):
    """
    Player gateway
    """

    def find_all(self) -> List[Player]:
        """
        Get all players

        :return:
        """

    def find(self, identifier: str) -> Optional[Player]:
        """
        Get a player by his identifier

        :return:
        """

    def persist(self, player: Player):
        """
        Persist a player

        :param player:
        :return:
        """
