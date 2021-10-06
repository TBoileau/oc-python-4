"""Imported modules/packages"""
from typing import List, Optional, Dict

from tinydb import TinyDB, Query
from tinydb.table import Table

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
        self.__players: Dict[str, Player] = {}

    def find_all(self) -> List[Player]:
        players: List[Player] = list(map(self.__player_factory.create, self.__table.all()))

        for player in players:
            self.__players[player.identifier.__str__()] = player

        return list(self.__players.values())

    def find(self, identifier: str) -> Optional[Player]:
        if identifier in self.__players:
            return self.__players[identifier]

        query: Query = Query()
        data: List[Dict] = self.__table.search(query.id == identifier)

        if len(data) == 0:
            return None

        self.__players[identifier] = self.__player_factory.create(data[0])

        return self.__players[identifier]

    def persist(self, player: Player):
        self.__table.insert(player.serialize())
        self.__players[player.identifier.__str__()] = player
