"""Imported modules/packages"""
from typing import List, Optional, Dict

from tinydb import TinyDB, Query
from tinydb.table import Table

from src.entity.tournament import Tournament
from src.factory.tournament_factory import TournamentFactoryInterface
from src.gateway.tournament_gateway import TournamentGateway


class TournamentRepository(TournamentGateway):
    """
    TournamentRepository class
    """

    def __init__(self, tiny_db: TinyDB, tournament_factory: TournamentFactoryInterface):
        self.__tournament_factory: TournamentFactoryInterface = tournament_factory
        self.__table: Table = tiny_db.table("tournaments")
        self.__tournaments: Dict[str, Tournament] = {}

    def find_all(self) -> List[Tournament]:
        tournaments: List[Tournament] = list(map(self.__tournament_factory.create, self.__table.all()))

        for tournament in tournaments:
            self.__tournaments[tournament.identifier.__str__()] = tournament

        return list(self.__tournaments.values())

    def find(self, identifier: str) -> Optional[Tournament]:
        if identifier in self.__tournaments:
            return self.__tournaments[identifier]

        query: Query = Query()
        data: List[Dict] = self.__table.search(query.id == identifier)

        if len(data) == 0:
            return None

        self.__tournaments[identifier] = self.__tournament_factory.create(data[0])

        return self.__tournaments[identifier]

    def persist(self, tournament: Tournament):
        self.__table.insert(tournament.serialize())
        self.__tournaments[tournament.identifier.__str__()] = tournament
