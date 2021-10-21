"""Imported modules/packages"""
from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.orm.repository import Repository

from src.entity.tournament import Tournament


class TournamentRepository(Repository):
    """
    TournamentRepository class
    """

    def __init__(self, entity_manager: EntityManagerInterface):
        super().__init__(entity_manager, Tournament, "tournaments")
