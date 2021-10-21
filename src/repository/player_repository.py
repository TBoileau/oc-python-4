"""Imported modules/packages"""
from lib.orm.entity_manager_interface import EntityManagerInterface
from lib.orm.repository import Repository

from src.entity.player import Player


class PlayerRepository(Repository):
    """
    PlayerRepository class
    """

    def __init__(self, entity_manager: EntityManagerInterface):
        super().__init__(entity_manager, Player, "players")
