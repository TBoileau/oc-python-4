"""Imported modules/packages"""
from datetime import date

from tinydb.table import Document

from src.entity.player import Player
from src.factory.player_factory_interface import PlayerFactoryInterface


class PlayerFactory(PlayerFactoryInterface):
    """
    Player factory
    """

    def create(self, data: Document) -> Player:
        return Player(
            identifier=data.doc_id,
            last_name=data["last_name"],
            first_name=data["first_name"],
            birthday=date.fromisoformat(data["birthday"]),
            gender=data["gender"],
            ranking=int(data["ranking"]),
        )
