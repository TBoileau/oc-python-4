"""Imported modules/packages"""
from abc import ABC
from typing import Dict

from src.entity.tournament import Tournament


class TournamentFactoryInterface(ABC):
    """
    Tournament factory interface
    """

    def create(self, data: Dict) -> Tournament:
        """
        Create an instance of Tournament

        :param data:
        :return:
        """
