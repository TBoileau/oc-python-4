"""Imported modules/packages"""
from typing import List, Optional, Dict

from tinydb import TinyDB
from tinydb.table import Table, Document

from src.entity.player import Player
from src.factory.player_factory import PlayerFactoryInterface
from src.gateway.player_gateway import PlayerGateway


class PlayerRepository(PlayerGateway):
    """
    PlayerRepository class
    """

    def __init__(self, tiny_db: TinyDB, player_factory: PlayerFactoryInterface):
        self.__player_factory: PlayerFactoryInterface = player_factory
        self.__table: Table = tiny_db.table("players")
        self.__players: Dict[int, Player] = {}

    def find_all(self) -> List[Player]:
        players: List[Player] = list(map(self.__player_factory.create, self.__table.all()))

        for player in players:
            if player.identifier not in self.__players:
                self.__players[player.identifier] = player

        return list(self.__players.values())

    def find(self, identifier: int) -> Optional[Player]:
        if identifier in self.__players:
            return self.__players[identifier]

        data: Optional[Document] = self.__table.get(doc_id=identifier)

        if data is None:
            return None

        self.__players[identifier] = self.__player_factory.create(data)

        return self.__players[identifier]

    def persist(self, player: Player):
        player.identifier = self.__table.insert(player.serialize())
        self.__players[player.identifier] = player
