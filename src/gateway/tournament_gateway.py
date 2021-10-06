"""Imported modules/packages"""
from abc import ABC
from typing import List, Optional

from src.entity.tournament import Tournament


class TournamentGateway(ABC):
    """
    Tournament gateway
    """

    def find_all(self) -> List[Tournament]:
        """
        Get all tournament

        :return:
        """

    def find(self, identifier: str) -> Optional[Tournament]:
        """
        Get a tournament by his identifier

        :return:
        """

    def persist(self, tournament: Tournament):
        """
        Persist a tournament

        :param tournament:
        :return:
        """
