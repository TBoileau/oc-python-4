"""Imported modules/packages"""
from typing import List, Optional, Dict

from tinydb import TinyDB
from tinydb.table import Table, Document

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
        self.__tournaments: Dict[int, Tournament] = {}

    def find_all(self) -> List[Tournament]:
        tournaments: List[Tournament] = list(map(self.__tournament_factory.create, self.__table.all()))

        for tournament in tournaments:
            self.__tournaments[tournament.identifier] = tournament

        return list(self.__tournaments.values())

    def find(self, identifier: int) -> Optional[Tournament]:
        if identifier in self.__tournaments:
            return self.__tournaments[identifier]

        data: Optional[Document] = self.__table.get(doc_id=identifier)

        if data is None:
            return None

        self.__tournaments[identifier] = self.__tournament_factory.create(data)

        return self.__tournaments[identifier]

    def persist(self, tournament: Tournament):
        tournament.identifier = self.__table.insert(tournament.serialize())
        self.__tournaments[tournament.identifier] = tournament
